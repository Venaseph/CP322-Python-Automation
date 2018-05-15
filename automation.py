# !/usr/bin/env python
import sys
import os
import subprocess
import time
import urllib.request
import hashlib


# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"
REPO_DIR = "cp332-project6"
RM_RF = "rm -rf "
START_TIME = time.ctime()
PIC_LINK = 'https://s3.amazonaws.com/southhills/pics/'

#Global Vars
testCaseResults = {'Run': 0, 'Pass': 0, 'Fail': 0}
version = None
revHash = None
# commands DataModel holds {key=scriptArg, [ExpStatusCode, PicComp, exMD5, acMD5, statusCode, log, commandRun]}
commands = {'dog': [0, 'pic1', 'exMD5', 'acMD5', 'stCode', 'log', 'commandRun'], 
            'ducks': [0, 'pic2', 'exMD5', 'acMD5', 'stCode', 'log', 'commandRun'],
            'flower': [0, 'pic3', 'exMD5', 'acMD5', 'stCode', 'log', 'commandRun'],
            'moon': [0, 'pic4', 'exMD5', 'acMD5', 'stCode', 'log', 'commandRun'], 
            'mountain': [0, 'pic5', 'exMD5', 'acMD5', 'stCode', 'log', 'commandRun'],
            ' ': [2, None, None, None, 'stCode', 'log', 'commandRun'],
            'sun': [2, None, None, None, 'stCode', 'log', 'commandRun']}


def main():
    # Remove Old / Get New
    gitIt()
    # Retrieve Repo Hash and Versions
    gitVersion()
    gitRevisionHash()
    getMD5s()
    testController()


    print(START_TIME)
    print(version)
    print(revHash)
    print(testCaseResults['Run'])


def testController():
    os.chdir(REPO_DIR)
    for key, value in commands.items():
        runScript(key, value)
        hashHandling(key, value)


def hashHandling(key, value):
    if value[]


def runScript(key, value):
    global testCaseResults
    testCaseResults['Run'] += 1
    try:
        value[5] = subprocess.check_output(['python', 'getpicture', key], stderr=subprocess.STDOUT).decode('utf-8')
        value[4] = 0
        # print(key + " " + output[:-1])
    except Exception as ex:
        value[5] = str(ex)
        string = str(ex)[-2:]
        value[4] = string[:-1]
        # print(key + " Failed: ", ex)
    # finally:
    #     print(value[4])


def getMD5s():
    global commands
    for key, value in commands.items():
        if value[1]:
            try:
                grabMD5 = urllib.request.urlopen('https://s3.amazonaws.com/southhills/pics/' + value[1] + '.md5')
                value[2] = grabMD5.read().decode('utf-8')
            except Exception as ex:
                value[2] = ex
            # finally:
            #     print(value[2])


def gitVersion():
    global version
    try:
        # Create var for opening the VERSION file in repo using os
        verFile = os.path.join(os.getcwd(), REPO_DIR, 'VERSION')
        with open(verFile, 'r') as versionFile:
            # Grab version, remove newline
            version = versionFile.read()[:-1]
    except Exception as ex:
        exceptionKillDef(ex)


def gitRevisionHash():
    global revHash
    # Grab long version of HEAD from repo to aquire the hash, remove /n and decode b object
    revHash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8') 


def gitIt():
    # Check for existing data / rm rf if exists
    rmrfOldData()
    try:
        # Clone Repo
        os.system(CLONE_REPO) 
        # not sure if this checks for the 128 failed exit code git returns on a bad download, inquire in class
        print("Repo Cloned Successfully!")
    except Exception as ex:
        exceptionKillDef(ex)


def rmrfOldData():
    # Check if directory exists
     if os.path.isdir(REPO_DIR): 
        # Recusively delete files and folders if it does
        os.system(RM_RF + REPO_DIR)   


def exceptionKillDef(ex):
    print(ex)
    with open('results.txt', 'a+') as results:
        results.write('\n------ START FAILURE-------\n')
        results.write(START_TIME + '\n')
        results.write(('Version: ' + version + '\n') if version else 'Version: Unavailable\n')
        results.write(('Hash: ' + revHash + '\n') if revHash else 'Hash: Unavailable\n')
        results.write('^^^^^^^ END FAILURE ^^^^^^^\n')
    sys.exit(1)        


if __name__ == "__main__":
    sys.exit(main())