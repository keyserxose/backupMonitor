#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import date
from datetime import datetime

# Reading from the current path
path = __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#os.environ['BORG_REPO'] = 'Here goes the env variable'

def backupRsync():
    jsonBackup = open('/home/xose/Scripts/backup/output.json')
    data = json.load(jsonBackup)
    format = "%Y-%m-%dT%H:%M:%S.%f"
    last_modified = data['repository']['last_modified']
    backupDate = datetime.strptime(last_modified, format)
    today = date.today()
    global dateBackup
    dateBackup = backupDate.date()
    global backup
    if today != dateBackup:
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Dates do not match, backup has not run!')
        backup = 'N'

    elif today == dateBackup:
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Backup has been completed!')
        backup = 'Y'

def backupLocal():
    jsonBackup = open('/home/xose/Scripts/backup/outputLocal.json')
    data = json.load(jsonBackup)
    format = "%Y-%m-%dT%H:%M:%S.%f"
    last_modified = data['repository']['last_modified']
    backupDate = datetime.strptime(last_modified, format)
    today = date.today()
    global dateBackup
    dateBackup = backupDate.date()
    global backupLocal
    if today != dateBackup:
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Dates do not match, backup has not run!')
        backupLocal = 'N'

    elif today == dateBackup:
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Backup has been completed!')
        backupLocal = 'Y'

# This consumes the json file from a url and prints the output

#url = 'http://localhost:8080/data.json'
#
#new_request = requests.get(url)
#json_data = new_request.json()

#print(json_data['Backup'])

# Test SMART Data

def checkDisks():
    disks = {'sda','sdb','sdc','sdd','sde'}

    for disk in disks:
        print('Checking disk /dev/'+disk)
        os.system('smartctl --all /dev/'+disk+' -j > /home/xose/sysReports/smartdata.json')
        report = open('/home/xose/sysReports/smartdata.json')
        jsonData = json.load(report)
        try:
            jsonOutput = jsonData['ata_smart_data']['self_test']['status']['string']
        except KeyError:
            pass
            
        global disk0
        global status0
        global disk1
        global status1
        global disk2
        global status2
        global disk3
        global status3
        global disk4
        global status4
        if jsonOutput == 'completed without error' and disk == 'sda':
            disk0 = disk
            status0 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdb':
            disk1 = disk
            status1 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdc':
            disk2 = disk
            status2 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdd':
            disk3 = disk
            status3 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sde':
            disk4 = disk
            status4 = 'Good'
        elif jsonOutput != 'completed without error' and disk == 'sda':
            disk0 = disk
            status0 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdb':
            disk1 = disk
            status1 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdc':
            disk2 = disk
            status2 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdd':
            disk3 = disk
            status3 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sde':
            disk4 = disk
            status4 = 'Issue'
        else:
            print('There is an issue!')
            pass



def generateJSON():
    apachedir = '/srv/http/'
    output = [{'backup0':{'backup': backup, 'date': str(dateBackup), 'device':'rsync'},
    'backup': {'backup1': backupLocal, 'date': str(dateBackup), 'device':'local'}},
    {'disk0':{'device': disk0, 'status': status0}, 
    'disk1':{'device': disk1, 'status': status1},
    'disk2':{'device': disk2, 'status': status2},
    'disk3':{'device': disk3, 'status': status3},
    'disk4':{'device': disk4, 'status': status4}},
    ]
    with open(apachedir+'data.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)


backupRsync()

backupLocal()

checkDisks()

generateJSON()

