# !/usr/bin/env python
import sys
import os
import subprocess


# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"
REPO_DIR = "cp332-project6"
RM_RF = "rm -rf "

#Global Vars
testCaseResults = {'Pass': 0, 'Fail': 0}
version = None
revHash = None


def main():
    # Remove Old / Get New
    gitIt()
    # Retrieve Repo Hash and Versions
    gitVersion()
    gitRevisionHash()

    print(version)
    print(revHash)


def gitVersion():
    global version

    os.chdir(REPO_DIR)
    try:
        with open('VERSION', 'r') as versionFile:
            # Grab version, remove newline
            version = versionFile.read()[:-1]
    except Exception as ex:
        exceptionKillDef(ex)


def gitRevisionHash():
    global revHash
    revHash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


def gitIt():
    rmrfOldData() # Check for existing data / rm rf if exists
    try:
        os.system(CLONE_REPO) # Clone Repo
        # not sure if this checks for the 128 failed exit code git returns on a bad download, inquire in class
        print("Repo Cloned Successfully!")
    except Exception as ex:
        exceptionKillDef(ex)


def rmrfOldData():
     if os.path.isdir(REPO_DIR): # Check if directory exists
        os.system(RM_RF + REPO_DIR) # Recusively delete files and folders if it does   


def exceptionKillDef(ex):
    print(ex)
    try:
        with open('results.txt', 'w+') as results: 
            results.write("------ START FAILURE-------")
            results.write(version if version else 'Version: Unavailable')
            results.write(revHash if revHash else 'Hash: Unavailable')
            results.write("^^^^^^^ END FAILURE ^^^^^^^")
    except:
        pass

    sys.exit(1)        


if __name__ == "__main__":
    sys.exit(main())