import subprocess
import os


def getEra(inputDir):
    era = ''
    if '2023B' in inputDir:
        era = '2023B'
    elif '2023C' in inputDir:
        era = '2023C'
    elif '2023D' in inputDir:
        era = '2023D'
    elif '2022' in inputDir:
        era = '2022'    
    return era    

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