import os
import time
import datetime as dt
import threading

# Enter The Name Of The Directorys Here
dir2backup = "worlds"
backupdir = "backups"


def backup():
    cdt = dt.datetime.now()
    name = cdt.strftime('%Y-%m-%d-%H-%M-%S')
    print(name + ": File ready to BackUp")
    os.system(f"zip -r {name}.zip {dir2backup}")
    os.system(f"mv {name}.zip {backupdir}")
    print("BackUp complete")


def autobackup():
    threading.Timer(30 * 60, autobackup).start()
    print("Next BackUp add to be BackedUp")
    backup()


def load(name):
    try:
        print("Loading Backup")
        os.system(f"rm -r {dir2backup}")
        os.system(f"cp {backupdir}/{name}.zip {dir2backup}")
        os.system(f"unzip {dir2backup}/{name}.zip")
        os.system(f"rm {dir2backup}/{name}.zip")
        print("Backup Loaded")
    except Exception as error:
        print(error)


def backuplist():
    os.system(f"cd {backupdir} && ls")


def commands(cmd):
    if cmd[0] == "b":
        print("Selected 'b'")
        backup()
    elif cmd[0] == "l":
        print("Selected 'l'")
        load(cmd[1])
    elif cmd[0] == "bl":
        print("Selected 'bl'")
        backuplist()
    else:
        print("wrong input try again")


print("Started BackUp Script")
cdt = dt.datetime.now()
m = cdt.strftime('%M')
s = cdt.strftime('%S')
sec = 0

if (int(m) == 0 or int(m) == 30) and (int(s) == 0):
    pass
elif int(m) < 30:
    sec = (30 - int(m)) * 60
    if int(s) != 0:
        sec += 60 - int(s)
        sec -= 60
else:
    sec = (60 - int(m)) * 60
    if int(s) != 0:
        sec += 60 - int(s)
        sec -= 60
fb = threading.Timer(sec, autobackup).start()

while 1:
    print("Type 'b'-Backup 'l'-Load Backup 'bl'-Backup List 'stop'-Stop")
    cmd = input("[*] > ")
    if cmd == "stop":
        break
    else:
        cmd = cmd.split(" ")
        commands(cmd)
