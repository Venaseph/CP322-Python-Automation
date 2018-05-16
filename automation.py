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
testCaseResults = {'Run': 0, 'scriptPass': 0, 'Pass': 0, 'Fail': 0}
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
    printResultsController()


def printResultsController():
    # platform independant folder back using sep/norm instead of pathjoin
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
    with open('results.txt', 'a+') as results:
        results.write('\n' + START_TIME)
        results.write('Version: ' + version)
        results.write(('Hash: ' + revHash)
        results.write('Ran: ' + str(testCaseResults['Run']) + '     Pass: ' + str(testCaseResults['Pass']) + '     Fail: ' + str(testCaseResults['Fail']))
        for key, value in commands.items():
            results.write('\nCommand: ' + value[6])
            results.write('Script Result: ' + value[5])
            results.write('MD5/JPG: ' + (value[3]))
    sys.exit(0)  

    print('\n' + START_TIME)
    print('Version: ' + version)
    print('Hash: ' + revHash)
    print('Ran: ' + str(testCaseResults['Run']) + '     Pass: ' + str(testCaseResults['Pass']) + '     Fail: ' + str(testCaseResults['Fail']))
    for key, value in commands.items():
        print('\nCommand: ' + value[6])
        print('Script Result: ' + value[5])
        print('MD5/JPG: ' + (value[3]))


def testController():
    #move to correct DIR
    os.chdir(REPO_DIR)
    for key, value in commands.items():
        runScript(key, value)
        hashHandling(key, value)


def hashHandling(key, value):

    #if expected exists and download was successful  
    if value[4] is 0 and value[2]:
        # get hash of downloaded picture with horrible file name creation as binary
        with open(('0000' + str(testCaseResults['scriptPass'] - 1) + '.jpg'), 'rb') as file:
            data = file.read()
            # Hexdigest it 
            acMD5 = hashlib.md5(data).hexdigest()
            # Comparision handling
            if value[2].decode('utf-8') == acMD5:
                testCaseResults['Pass'] += 1
                value[3] = 'Match'
            else:
                testCaseResults['Fail'] += 1
                value[3] = 'Fail'
    else:
        value[3] = 'N/A'


def runScript(key, value):
    # global testCaseResults, commands
    # Incr total cases run
    testCaseResults['Run'] += 1
    value[6] = 'python getpicture ' + key
    try:
        # Run script test / Save log results
        value[5] = subprocess.check_output(['python', 'getpicture', key], stderr=subprocess.STDOUT).decode('utf-8')[:-1]
        # Record Success
        value[4] = 0
        # Incr scriptPass Counter
        testCaseResults['scriptPass'] += 1
    except Exception as ex:
        # Save log results
        value[5] = str(ex)
        string = str(ex)[-2:]
        # Save statusCode
        value[4] = string[:-1]
        # Increment fail counter
        testCaseResults['Fail'] += 1


def getMD5s():
    global commands
    for key, value in commands.items():
        if value[1]:
            try:
                grabMD5 = urllib.request.urlopen('https://s3.amazonaws.com/southhills/pics/' + value[1] + '.md5')
                value[2] = grabMD5.read()[:-1]
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