# !/usr/bin/env python
import sys
import os

# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"
REPO_DIR = "cp332-project6"
RM_REPO = "rm -rf "

def main():
    gitIt()


def gitIt():
    if os.path.isdir(REPO_DIR): # Check if directory exists
        os.system(RM_REPO + REPO_DIR) # Recusively delete files and folders if it does
    try:
        os.system(CLONE_REPO) # Clone Repo
        print("Repo Cloned Successfully!")
    except Exception as ex:
        exceptionDef(ex)


def exceptionDef(ex):
    print(ex)        


if __name__ == "__main__":
    sys.exit(main())