import subprocess
import os


def checkMakeDir( folder ):
    if not os.path.exists( folder ):
        os.mkdir( folder )
        
# def getPath()

def runCommand(command):
    print('runing command: ', command)
    process = subprocess.run( command, shell=True ) 
    output = process.stdout
    print(output)
    print('Done running command\n\n')