import os, time
import datetime as dt

#Enter The Name Of The Directorys Here
dir2backup = ""
backupdir = ""

def backup():
    cdt = dt.datetime.now()
    name = cdt.strftime('%Y-%m-%d-%H-%M-%S')
    os.system(f"zip -r {name}.zip {dir2backup}/*")
    os.system(f"mv {name}.zip {backupdir}")

def autobackup():
    cdt = dt.datetime.now()
    time.sleep(1)
    cdt = cdt.strftime('%M-%S')
    if cdt == "00-01":
        backup()

def load(name):
    try:
        os.system("rm -r worlds/*")
        os.system(f"cp backups/{name}.zip {dir2backup}")
        os.system(f"unzip {dir2backup}/{name}.zip")
        os.system(f"rm {dir2backup}/{name}.zip")
    except Exception as error:
        print(error)

def backuplist():
    os.system("cd backups && ls")

def commands(cmd):
    if cmd[0] == "b":
        backup()
    if cmd[0] == "l":
        load(cmd[1])
    if cmd[0] == "bl":
        backuplist()

print("[*] Started")
while 1:
    try:
        autobackup()
    except (KeyboardInterrupt, SystemExit):
        cmd = input("[*] > ")
        if cmd == "stop":
            print("[*] Stoping")
            break
        else:
            cmd = cmd.split(" ")
            commands(cmd)
    
