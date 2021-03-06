import os
import datetime as dt
import threading
import json

global dir2backup, backupdir, autobptime, autodltime


def backup():
    cdt = dt.datetime.now()
    name = cdt.strftime('%Y-%m-%d-%H-%M')
    print(name + ": File ready to BackUp")
    os.system(f"zip -r -q -T {name}.zip {dir2backup}")
    os.system(f"mv {name}.zip {backupdir}")
    print("BackUp complete")


def autobackup():
    global backupThread
    global oldbackupThread
    oldbackupThread = backupThread
    s = int(dt.datetime.now().strftime('%S'))
    if s == 0:
        backupThread = threading.Timer(int(autobptime) * 60, autobackup).start()
    elif s < 30:
        backupThread = threading.Timer((int(autobptime) * 60) - s, autobackup).start()
    else:
        backupThread = threading.Timer(int(autobptime) * 60, autobackup).start()
        print("Time out of sync in AutoBackup")

    backup()


def load(name):
    try:
        print("Loading Backup")
        os.system(f"rm -r {dir2backup}/*")
        os.system(f"cp {backupdir}/{name} {dir2backup}")
        os.system(f"unzip {dir2backup}/{name}")
        os.system(f"rm {dir2backup}/{name}")
        print("Backup Loaded")
    except Exception as error:
        print(error)


def backuplist():
    os.system(f"cd {backupdir} && ls")


def RemoveOldBackup():
    global deleteThread
    global olddeleteThread
    olddeleteThread = deleteThread
    s = int(dt.datetime.now().strftime('%S'))
    if s == 0:
        deleteThread = threading.Timer(30 * 60, RemoveOldBackup).start()
    elif s < 30:
        deleteThread = threading.Timer((30 * 60) - s, RemoveOldBackup).start()
    else:
        deleteThread = threading.Timer(30 * 60, RemoveOldBackup).start()
        print("Time out of sync in AutoRemove")
    if autodltime == "":
        print("remove canceled")
        return
    before3Days = dt.datetime.now() - dt.timedelta(days=int(autodltime))
    m = int(before3Days.strftime('%M'))
    h = int(before3Days.strftime('%H'))
    dateToRemove = before3Days.strftime('%Y-%m-%d-%H-%M')
    if m == 30:
        print("deleting: " + dateToRemove)
    elif h % 2 == 1:
        before4Days = dt.datetime.now() - dt.timedelta(days=int(autodltime) + 1)
        dateToRemove = before4Days.strftime('%Y-%m-%d-%H-%M')
        print("deleting: " + before4Days.strftime('%Y-%m-%d-%H-%M'))
    elif h != 0:
        before5Days = dt.datetime.now() - dt.timedelta(days=int(autodltime) + 2)
        dateToRemove = before5Days.strftime('%Y-%m-%d-%H-%M')
        print("deleting: " + before5Days.strftime('%Y-%m-%d-%H-%M'))
    os.system(f"rm {backupdir}/{dateToRemove}.zip")


def commands(cmd):
    if cmd[0] == "b":
        backup()
    elif cmd[0] == "l":
        load(cmd[1])
    elif cmd[0] == "bl":
        backuplist()
    elif cmd[0] == "e":
        setup()
    else:
        print("wrong input try again")


def setup():
    global dir2backup
    dir2backup = input('[*] Enter the name of directory to backup >')
    global backupdir
    backupdir = input('[*] Enter the name of directory to store the backups >')
    global autobptime
    print("Auto delete will nor work if time is not set to 30")
    autobptime = input('[*] Enter the time to take auto backup "Multiples of 30 Minutes only">')
    global autodltime
    if int(autobptime) == 30:
        autodltime = input('[*] Enter the time to delete older backups "In Days">')
    else:
        autodltime = ""

    configdefaultdata = {}
    with open('config.json', 'w') as defaultconfig:
        configdefaultdata['data'] = {
            "Directory2Backup": f"{dir2backup}",
            "BackupsDirectory": f"{backupdir}",
            "AutoBackupTime": f"{autobptime}",
            "AutoDeleteTime": f"{autodltime}"
        }
        json.dump(configdefaultdata, defaultconfig, indent=4)


def loadConfig():
    try:
        with open('config.json', 'r') as config:
            config = json.load(config)

            data = config['data']

            global dir2backup
            dir2backup = data['Directory2Backup']
            global backupdir
            backupdir = data['BackupsDirectory']
            global autobptime
            autobptime = int(data['AutoBackupTime'])
            global autodltime
            autodltime = int(data['AutoDeleteTime'])
        print("config loaded")
    except Exception as e:
        if str(e) == "[Errno 2] No such file or directory: 'config.json'":
            print("[*] Your config file is missing")
            setup()
        else:
            print(f'error = {e}')


print("Started BackUp Script")
cdt = dt.datetime.now()
m = int(cdt.strftime('%M'))
s = int(cdt.strftime('%S'))
sec = 0

loadConfig()

if (m == 0 or m == 30) and (s == 0):
    pass
elif m < 30:
    sec = (30 - m) * 60
    if s != 0:
        sec += 60 - s
        sec -= 60
else:
    sec = (60 - m) * 60
    if s != 0:
        sec += 60 - s
        sec -= 60
global backupThread
backupThread = threading.Timer(sec, autobackup).start()
global deleteThread
deleteThread = threading.Timer(sec, RemoveOldBackup).start()

while 1:
    print("Type 'b'-Backup, 'l'-Load backup, 'bl'-Backup list, 'e'-Edit backup config, 'stop'-Stop")
    cmd = input("[*] > ")
    if cmd == "stop":
        break
    else:
        cmd = cmd.split(" ")
        commands(cmd)
