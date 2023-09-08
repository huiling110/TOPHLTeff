import os

import usefulFunc as uf

def main():
    inputList = 'input/Muon2023B.txt'
    era = '2023B'
    # inputList = 'input/Muon2023C.txt'
    # era = '2023C'
    # inputList = 'input/Muon2023D.txt'
    # era = '2023D'
    # inputList = 'input/Moun2022.txt'
    # era = '2022'
    
    # jobVersion = 'v1ForHardronic'
    jobVersion = 'v1forEle'
    #!!!add parameter here to contral 
   
    outDir = makeOutDir(era, jobVersion)
     
    inList = getListFromTxt(inputList)
    # print(inList)
    nanoFileNum = len(inList)
    print( 'fileNum=', nanoFileNum)
   
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    jobDir = getNameFromPath(inputList)
    print('jobVersion: ', jobDir + jobVersion)
    jobDir = current_directory+ '/jobs/'+jobDir + '/'
    logDir = jobDir + 'logs/'
    uf.checkMakeDir(jobDir)
    uf.checkMakeDir(logDir)
    print(jobDir)
    
    writeJob( jobDir+'singleJob.sh', inputList, outDir)
    writeSub(jobDir +'subList.sub', jobDir, nanoFileNum)
    
    subHTCondor(jobDir+'subList.sub')  
    
def makeOutDir(era, jobVersion):
    outBase = '/eos/user/h/hhua/forTopHLT/'
    outDir = outBase + era +'/'
    uf.checkMakeDir(outDir)
    outDir = outDir + jobVersion + '/'
    uf.checkMakeDir(outDir)
    return outDir
    
def subHTCondor(subScript):
    #https://batchdocs.web.cern.ch/local/quick.html
    command = 'condor_submit {}'.format(subScript)
    uf.runCommand(command)
      
 
 
 
  
def getListFromTxt(inFile):
    # if not os.path.exists(file_path): 
    #     print(inFile, ' not exist!!!')
    with open(inFile, 'r') as file:
        # Read each line and store it in a list
        # lines = file.readlines()
        lines = [line.strip() for line in file]
        # print(lines)
    return lines
    
#generic functions that need to be grouped
def getNameFromPath(file_path):
    base_file_name = os.path.basename(file_path)
    # Remove the '.txt' postfix
    file_name_without_extension = os.path.splitext(base_file_name)[0]
    return file_name_without_extension
    

def writeJob( jobName, inFile, jobDir):
    lines = [
        '#!/bin/bash',
        'cd /afs/cern.ch/work/h/hhua/HLTStudy/TOPHLTeff/',
        'lines=(`cat /afs/cern.ch/work/h/hhua/HLTStudy/TOPHLTeff/{}`)'.format(inFile),
        'echo ${lines[$1]}',
        'python3 skimNano.py --arg1 ${lines[$1]} ' + ' --arg2 {}  --arg3 True '.format(jobDir),

    ]
    writeListToFile(lines, jobName)

def writeSub(subName, jobDir, fileNum):
    lines = [
        'arguments               = $(Process)',
        'executable              = {}singleJob.sh'.format(jobDir),
        'output                  = {}/logs/$(Process).out'.format(jobDir),
        'error                   = {}/logs/$(Process).err'.format(jobDir),
        'log                     = {}/logs/log.log'.format(jobDir),
        '+JobFlavour             = "workday"',
        'use_x509userproxy = true',
        'x509userproxy = /afs/cern.ch/user/h/hhua/.x509up_117245',
        'should_transfer_files   = YES',
        'when_to_transfer_output = ON_EXIT',
        'queue {}  '.format(fileNum),
    ]
    writeListToFile(lines, subName)
        

#!!!generic    
def writeListToFile(lines, file_path):
    try:
        with open(file_path, 'w') as file:
            for item in lines:
                file.write(item + '\n')
        print(f"Data written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error writing to '{file_path}': {str(e)}") 
   
def subSingleJob():
    command = 'condor_submit hello.sub'  
    
    
if __name__=='__main__':
    main() 