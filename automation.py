# !/usr/bin/env python
import sys
import os
import subprocess


# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"
REPO_DIR = "cp332-project6"
RM_RF = "rm -rf "


def main():
    # Remove Old / Get New
    gitIt()
    revHash = gitRevisionHash()
    print(revHash)


def gitRevisionHash():
    # Move to correct DIR
    os.chdir(REPO_DIR)
    # return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


def gitIt():
    rmrfOldData() # Check for existing data / rm rf if exists
    try:
        os.system(CLONE_REPO) # Clone Repo
        print("Repo Cloned Successfully!")
    except Exception as ex:
        exceptionDef(ex)


def rmrfOldData():
     if os.path.isdir(REPO_DIR): # Check if directory exists
        os.system(RM_RF + REPO_DIR) # Recusively delete files and folders if it does   


def exceptionDef(ex):
    print(ex)        


if __name__ == "__main__":
    sys.exit(main())