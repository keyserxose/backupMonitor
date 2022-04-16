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

#a = os.system('borg list --last 1 --json > output.json')

# This reads the output.json and compares the date
#f = open(path+'/output.json')

apachedir = '/srv/http/'

f = open('/home/xose/Scripts/backups/output.json')
 
data = json.load(f)

format = "%Y-%m-%dT%H:%M:%S.%f"

last_modified = data['repository']['last_modified']

backup = datetime.strptime(last_modified, format)

date = date.today()

dateBackup = backup.date()

if date != dateBackup:
    print('This is the current date: '+str(date))
    print('This is the date of the last backup: '+str(dateBackup))
    print('Dates do not match, backup has not run!')
    output = {
    "Backup" : "N"
}

elif date == dateBackup:
    print('This is the current date: '+str(date))
    print('This is the date of the last backup: '+str(dateBackup))
    print('Backup has been completed!')
    output = {
    "Backup" : "Y"
}

# This generates a json file

with open(apachedir+'data.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)

# This consumes the json file from a url and prints the output

url = 'http://localhost:8080/data.json'

new_request = requests.get(url)
json_data = new_request.json()

#print(json_data['Backup'])

# Test SMART Data

disks = {'sda','sdb','sdc','sdd','sde'}

for disk in disks:
    print('Checking disk /dev/'+disk)
    os.system('smartctl --all /dev/'+disk+' -j > /home/xose/sysReports/smartdata.json')
    report = open('/home/xose/sysReports/smartdata.json')
    jsonData = json.load(report)
    jsonOutput = jsonData['ata_smart_data']['self_test']['status']['string']
    #print(jsonOutput)
    if jsonOutput == 'completed without error':
        print('No Errors')
    else:
        print('Disk has issue!')
        pass