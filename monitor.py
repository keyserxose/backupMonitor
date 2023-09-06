#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import date
from datetime import datetime
from datetime import timedelta

# Reading from the current path
path = __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

mirrorLog = '/home/xose/Scripts/backup/backup.log'
global partitions
partitions = {'sdb6','sdb7','sda1','sdc1','sdd1'}
global disks
disks = {'sda','sdb','sdc','sdd'}

def mirror():
    global mirror
    today = date.today()
    today = today.strftime("%Y/%m/%d")
    backupDate = os.popen('cat '+mirrorLog+' | head -c 10').read()
    error = os.popen('cat '+mirrorLog+' | grep error').read()
    if today == backupDate and 'error' in error:
        mirror = '<div style="color:red">&#9632;</div>'
        print('There is an error, backup has not run!')
    elif today == backupDate:
      mirror = '<div style="color:green">&#9632;</div>'
      print('Backup has been completed!')
    else:
      mirror = '<div style="color:red">&#9632;</div>'
      print('There is an error, backup has not run!')
        

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


def quota():
  jsonQuota = open('/home/xose/Scripts/backup/quota.json')
  data = json.load(jsonQuota)
  global usage
  usage = data['quota'][0]['usage']
  global hardquota
  hardquota = data['quota'][0]['hardquota']
  result = float(hardquota) - float(usage)
  global resultF
  resultF = "{:.0f}".format(result)

quota()

def checkSpaceDisk():
    for disk in partitions:
        print('Checking disk /dev/'+disk)
        avail = os.popen('df -h --output=avail /dev/'+disk+' | tail -1').read()
        target = os.popen('df -h --output=target /dev/'+disk+' | tail -1').read()
        print(avail)

        global avail0
        global target0
        global avail1
        global target1
        global avail2
        global target2
        global avail3
        global target3
        global avail4
        global target4
        global avail5
        global target5

        if disk == 'sdb6':
            part0 = disk
            avail0 = avail
            target0 = target
        elif disk == 'sdb7':
            part1 = disk
            avail1 = avail
            target1 = target
        elif disk == 'sda1':
            part2 = disk
            avail2 = avail
            target2 = target
        elif disk == 'sdd1':
            part3 = disk
            avail3 = avail
            target3 = target
        elif disk == 'sdc1':
            part4 = disk
            avail4 = avail
            target4 = target
        else:
            pass



checkSpaceDisk()

# Test SMART Data

def checkDisks():
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
        global avail0
        global disk1
        global status1
        global disk2
        global status2
        global disk3
        global status3
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
        else:
            print('There is an issue with disk /dev/'+disk)
            pass


def checkDisksAge():
    #disks = {'sda','sdb','sdc','sdd','sde'}
    for disk in disks:
        print('Checking disk /dev/'+disk)
        os.system('smartctl --all /dev/'+disk+' -j > /home/xose/sysReports/smartdata.json')
        report = open('/home/xose/sysReports/smartdata.json')
        jsonData = json.load(report)
        try:
          powerOn = jsonData['power_on_time']['hours']
        except KeyError:
          pass
        d = timedelta(hours=powerOn)
        numMonths = int(d.days/30)
        if numMonths > 12 and numMonths < 24:
          print('Powered On: 1 year, '+str(numMonths - 12)+' months')
          age = '1 year, '+str(numMonths - 12)+' months'
        elif (numMonths) < 12:
          print('Powered On: '+str(numMonths)+' months')
          age = str(numMonths)+' months'
        elif numMonths >= 24:
          print('Powered On: 2 year, '+str(numMonths - 24)+' months')
          age = '2 year, '+str(numMonths - 24)+' months'

        global age0
        global age1
        global age2
        global age3
        global age4
        if disk == 'sda':
            disk0 = disk
            age0 = age
        elif disk == 'sdb':
            disk1 = disk
            age1 = age
        elif disk == 'sdc':
            disk2 = disk
            age2 = age
        elif disk == 'sdd':
            disk3 = disk
            age3 = age
        


checkDisksAge()

def generateJSON():
    apachedir = '/srv/http/'
    output = [
    {'backup0':{'backup': backup0, 'date': str(dateBackup), 'destination':dest0},
    'backup1': {'backup': backup1, 'date': str(dateBackup), 'destination':dest1}},
    {'disk0':{'device': disk0, 'status': status0, 'age': age0}, 
    'disk1':{'device': disk1, 'status': status1, 'age': age1},
    'disk2':{'device': disk2, 'status': status2, 'age': age2},
    'disk3':{'device': disk3, 'status': status3, 'age': age3}},
    ]
    with open(apachedir+'data.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)

mirror()

backup('rsync')

backup('local')

checkDisks()

generateJSON()


sysReports = '/home/xose/sysReports/'

s = open(sysReports+'style.css', 'w')

css = """body{

    background-color: #f2f2f2;
    font-family: 'Source Sans Pro', sans-serif;
    color: #222222
}

h1{
    
    margin-left: 1100;
}

table{

    font-weight: bold;
    font-size: 40px;
    margin-left: 20px;
    /*margin-left: 1100;*/
}

#tableDisks{

    position: fixed;
    margin-left: 70px;
}

th{

    font-weight: bold;
}"""


# writing the code into the file
s.write(css)
  
# close the file
s.close()


f = open(sysReports+'index.html', 'w')

html = """<html>
<head>
<title>System Monitor</title>
<link rel= 'stylesheet' type='text/css' href='style.css'/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200&display=swap" rel="stylesheet">
<meta http-equiv="refresh" content="300" >
</head>
<body>
<h1>System Monitor</h1>

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
    <th>Powered On</th>
  </tr>
  <tr>
    <td>"""+disk0+"""</td>
    <td></td>
    <td>"""+status0+"""</td>
    <td>"""+age0+"""</td>
  </tr>
  <tr>
    <td>"""+disk1+"""</td>
    <td></td>
    <td>"""+status1+"""</td>
    <td>"""+age1+"""</td>
  </tr>
  <tr>
    <td>"""+disk2+"""</td>
    <td></td>
    <td>"""+status2+"""</td>
    <td>"""+age2+"""</td>
  </tr>
  <tr>
    <td>"""+disk3+"""</td>
    <td></td>
    <td>"""+status3+"""</td>
    <td>"""+age3+"""</td>
  </tr>
</table>

<p></p>

<table>
  <tr>
    <th>Available</th>
    <th></th>
    <th id='tableDisks'>Partition</th>
  </tr>
  <tr>
    <td>&nbsp;"""+str(avail0)+"""</td>
    <td></td>
    <td id='tableDisks'>"""+target0+"""</td>
  </tr>
  <tr>
    <td>&nbsp;"""+str(avail1)+"""</td>
    <td></td>
    <td id='tableDisks'>"""+target1+"""</td>
  </tr>
  <tr>
    <td>&nbsp;"""+str(avail2)+"""</td>
    <td></td>
    <td id='tableDisks'>"""+target2+"""</td>
  </tr>
  <tr>
    <td>&nbsp;"""+str(avail3)+"""</td>
    <td></td>
    <td id='tableDisks'>"""+target3+"""</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;"""+resultF+"""G</td>
    <td></td>
    <td id='tableDisks'>rsync.net</td>
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
    os.system('cp -p -R '+sysReports+'index.html ' +sysReports+'style.css /srv/http/')

copyToApache()