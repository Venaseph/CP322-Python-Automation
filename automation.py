# !/usr/bin/env python
import sys
import os

# Global Constants
CLONE_REPO = "git clone https://github.com/ccoble-southhills/cp332-project6.git"

def main():
    gitIt()


def gitIt():
    #os.system("sshpass -p your_password ssh user_name@your_localhost")
    #os.chdir(REPO_PATH) # Move to Clone folder
    try:
        os.system(CLONE_REPO) # Clone Repo
        print("Repo Cloned Successfully!")
    except Exception as ex:
        exceptionDef(ex)


def exceptionDef(ex):
    print(ex)        


if __name__ == "__main__":
    sys.exit(main())