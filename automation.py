# !/usr/bin/env python
import sys
import os
import subprocess
import time


# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"
REPO_DIR = "cp332-project6"
RM_RF = "rm -rf "
START_TIME = time.ctime()
PIC_LINK = 'https://s3.amazonaws.com/southhills/pics/'

#Global Vars
testCaseResults = {'Attempts': 0, 'Pass': 0, 'Fail': 0}
version = None
revHash = None
# commands Dictonary holds {key=scriptArg, [ExpStatusCode, runtime, md5sum, ]}
commands = {'dog': [0, 'pic1'], 
            'ducks': [0, 'pic2'],
            'flower': [0, 'pic3'],
            'moon': [0, 'pic4'], 
            'mountain': [0, 'pic5'],
            ' ': [2],
            'sun': [2]}


def main():
    # Remove Old / Get New
    gitIt()
    # Retrieve Repo Hash and Versions
    gitVersion()
    gitRevisionHash()
    testController()


    print(START_TIME)
    print(version)
    print(revHash)


def testController():
    global commands
    os.chdir(REPO_DIR)
    for key, value in commands.items():
        runScript(key, value)


def runScript(key, value):

    arg = key
    try:
        print(os.getcwd())
        output = subprocess.check_output(['python', 'getpicture', arg], stderr=subprocess.STDOUT).decode('utf-8')
        print(output)
    except Exception as ex:
        print(key + " failed: ", ex)

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