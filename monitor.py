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

mirrorLog = '/home/xose/Scripts/backup/backup.log'

def mirror():
    global mirror
    if os.path.exists(mirrorLog):
        mirror = '<div style="color:red">&#9632;</div>'
    else:
        mirror = '<div style="color:green">&#9632;</div>'

def backup(dest):
    global dest0
    global dest1
    global jsonBackup
    if dest == 'rsync':
        jsonBackup = open('/home/xose/Scripts/backup/output'+dest+'.json')
        dest0 = dest
    elif dest == 'local':
        jsonBackup = open('/home/xose/Scripts/backup/output'+dest+'.json')
        dest1 = dest
    else:
        pass
    data = json.load(jsonBackup)
    format = "%Y-%m-%dT%H:%M:%S.%f"
    last_modified = data['repository']['last_modified']
    backupDate = datetime.strptime(last_modified, format)
    today = date.today()
    global dateBackup
    dateBackup = backupDate.date()
    global backup0
    global backup1
    if today != dateBackup and dest == 'rsync':
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Dates do not match, backup has not run!')
        backup0 = '<div style="color:red">&#9632;</div>'

    elif today == dateBackup and dest == 'rsync':
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Backup has been completed!')
        backup0 = '<div style="color:green">&#9632;</div>'
    
    elif today != dateBackup and dest == 'local':
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Dates do not match, backup has not run!')
        backup1 = '<div style="color:red">&#9632;</div>'

    elif today == dateBackup and dest == 'local':
        print('This is the current date: '+str(today))
        print('This is the date of the last backup: '+str(dateBackup))
        print('Backup has been completed!')
        backup1 = '<div style="color:green">&#9632;</div>'


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
            status0 = '<div style="color:green">&#9632;</div>'
        elif jsonOutput == 'completed without error' and disk == 'sdb':
            disk1 = disk
            status1 = '<div style="color:green">&#9632;</div>'
        elif jsonOutput == 'completed without error' and disk == 'sdc':
            disk2 = disk
            status2 = '<div style="color:green">&#9632;</div>'
        elif jsonOutput == 'completed without error' and disk == 'sdd':
            disk3 = disk
            status3 = '<div style="color:green">&#9632;</div>'
        elif jsonOutput == 'completed without error' and disk == 'sde':
            disk4 = disk
            status4 = '<div style="color:green">&#9632;</div>'
        elif jsonOutput != 'completed without error' and disk == 'sda':
            disk0 = disk
            status0 = '<div style="color:red">&#9632;</div>'
        elif jsonOutput != 'completed without error' and disk == 'sdb':
            disk1 = disk
            status1 = '<div style="color:red">&#9632;</div>'
        elif jsonOutput != 'completed without error' and disk == 'sdc':
            disk2 = disk
            status2 = '<div style="color:red">&#9632;</div>'
        elif jsonOutput != 'completed without error' and disk == 'sdd':
            disk3 = disk
            status3 = '<div style="color:red">&#9632;</div>'
        elif jsonOutput != 'completed without error' and disk == 'sde':
            disk4 = disk
            status4 = '<div style="color:red">&#9632;</div>'
        else:
            print('There is an issue with disk /dev/'+disk)
            pass



def generateJSON():
    apachedir = '/srv/http/'
    output = [
    {'backup0':{'backup': backup0, 'date': str(dateBackup), 'destination':dest0},
    'backup1': {'backup': backup1, 'date': str(dateBackup), 'destination':dest1}},
    {'disk0':{'device': disk0, 'status': status0}, 
    'disk1':{'device': disk1, 'status': status1},
    'disk2':{'device': disk2, 'status': status2},
    'disk3':{'device': disk3, 'status': status3},
    'disk4':{'device': disk4, 'status': status4}},
    ]
    with open(apachedir+'data.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)

mirror()

backup('rsync')

backup('local')

checkDisks()

generateJSON()


############THIS IS A TEST##############

#f = open('/srv/http/index.html', 'w')

f = open('index.html', 'w')
  
# the html code which will go in the file GFG.html
html = """<html>
<head>
<title>Title</title>
<link rel= 'stylesheet' type='text/css' href='style.css'/>
</head>
<body>
<h1>Computer Status</h1>

<table>
  <tr>
    <th>Backup</th>
    <th></th>
    <th>Status</th>
  </tr>
  <tr>
    <td>Rsync</td>
    <td></td>
    <td>"""+backup0+"""</td>
  </tr>
  <tr>
    <td>Local</td>
    <td></td>
    <td>"""+backup1+"""</td>
  </tr>
  <tr>
    <td>Mirror</td>
    <td></td>
    <td>"""+mirror+"""</td>
  </tr>
</table>
  
<p></p>


<table>
  <tr>
    <th>Disk</th>
    <th></th>
    <th>Status</th>
  </tr>
  <tr>
    <td>"""+disk0+"""</td>
    <td></td>
    <td>"""+status0+"""</td>
  </tr>
  <tr>
    <td>"""+disk1+"""</td>
    <td></td>
    <td>"""+status1+"""</td>
  </tr>
  <tr>
    <td>"""+disk2+"""</td>
    <td></td>
    <td>"""+status2+"""</td>
  </tr>
  <tr>
    <td>"""+disk3+"""</td>
    <td></td>
    <td>"""+status3+"""</td>
  </tr>
  <tr>
    <td>"""+disk4+"""</td>
    <td></td>
    <td>"""+status4+"""</td>
  </tr>
</table>

</body>
</html>
"""

 
# writing the code into the file
f.write(html)
  
# close the file
f.close()

def copyToApache():
    #os.system('cp style.css paper/')
    #os.system('chmod -R 777 paper')
    os.system('cp -p -R index.html /srv/http/')

copyToApache()