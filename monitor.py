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

def backupStatus():
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
        jsonOutput = jsonData['ata_smart_data']['self_test']['status']['string']
        global disk1
        global status1
        global disk2
        global status2
        global disk3
        global status3
        global disk4
        global status4
        global disk5
        global status5
        if jsonOutput == 'completed without error' and disk == 'sda':
            disk1 = disk
            status1 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdb':
            disk2 = disk
            status2 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdc':
            disk3 = disk
            status3 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sdd':
            disk4 = disk
            status4 = 'Good'
        elif jsonOutput == 'completed without error' and disk == 'sde':
            disk5 = disk
            status5 = 'Good'
        elif jsonOutput != 'completed without error' and disk == 'sda':
            disk1 = disk
            status1 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdb':
            disk2 = disk
            status2 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdc':
            disk3 = disk
            status3 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sdd':
            disk4 = disk
            status4 = 'Issue'
        elif jsonOutput != 'completed without error' and disk == 'sde':
            disk5 = disk
            status5 = 'Issue'
        else:
            print('There is an issue!')
            pass



def generateJSON():
    apachedir = '/srv/http/'
    output = [{'Backup': backup, 'Backups Date': str(dateBackup)}, 
    {'Disk1':{'Device': disk1, 'Status': status1}, 'Disk2':{'Device': disk2, 'Status': status2}, 'Disk3':{'Device': disk3, 'Status': status3}, 'Disk4':{'Device': disk4, 'Status': status4}, 'Disk5':{'Device': disk5, 'Status': status5}},
    ]
    with open(apachedir+'data.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)


backupStatus()

checkDisks()

generateJSON()

