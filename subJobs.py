import os

import usefulFunc as uf

def main():
    # inputList = 'input/Muon2023B.txt'
    # era = '2023B'
    # inputList = 'input/Muon2023C.txt'
    # era = '2023C'
    # inputList = 'input/Muon2023D.txt'
    # era = '2023D'
    # inputList = 'input/Muon2022.txt'
    # era = '2022'
    # inputList = 'input/Muon2024C.txt'
    # era = '2024C'
    # inputList = 'input/Muon2024D.txt'
    inputList = 'input/Muon2024D_all.txt'
    # era = '2024DpreCalib'
    era = '2024D'
    isVictor = False
    # jobVersion = 'v1ForHadronic'
    # jobVersion = 'v1ForEle'
    jobVersion = 'v2HadronicWithRdataframe'
  
  
  
   
    outDir = makeOutDir(era, jobVersion)
     
    inList = getListFromTxt(inputList)
    # print(inList)
    nanoFileNum = len(inList)
    print( 'fileNum=', nanoFileNum)
   
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    name = getNameFromPath(inputList)
    uf.checkMakeDir(current_directory+ '/jobs/')
    print('jobVersion: ', name + jobVersion)
    # jobDir = current_directory+ '/jobs/'+jobDir + '/' + jobVersion + '/'
    jobDir = current_directory+ '/jobs/'+name + '/' + jobVersion + '/'
    logDir = jobDir + 'logs/'
    uf.checkMakeDir(current_directory + '/jobs/' + name + '/')
    uf.checkMakeDir(jobDir)
    uf.checkMakeDir(logDir)
    print(jobDir)
    
    writeJob( jobDir+'singleJob.sh', inputList, outDir)
    writeSub(jobDir +'subList.sub', jobDir, nanoFileNum)
    
    subHTCondor(jobDir+'subList.sub')  
    
# def makeOutDir(era, jobVersion):
def makeOutDir(era, jobVersion, isVictor=False):
    #outBase = '/eos/user/h/hhua/forTopHLT/'
    outBase = '/eos/user/v/vshang/forTopHLT_05072024/' if isVictor else '/eos/user/h/hhua/forTopHLT/'
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
    current_script_path = os.path.abspath(__file__)

# Get the directory containing the current script
    current_script_dir = os.path.dirname(current_script_path)
    lines = [
        '#!/bin/bash',
        f'cd {current_script_dir}',
        # 'lines=(`cat /afs/cern.ch/user/v/vshang/public/TOPHLTeff/{}`)'.format(inFile),
        f'lines=(`cat {current_script_dir}/{inFile}`)',
        'echo ${lines[$1]}',
        'python3 skimNano.py --arg1 ${lines[$1]} ' + ' --arg2 {}  --arg3 True '.format(jobDir),

    ]
    writeListToFile(lines, jobName)

def writeSub(subName, jobDir, fileNum, isVictor=False):
    proxyDir = 'h/hhua' if not isVictor else 'v/vshang'
    lines = [
        'arguments               = $(Process)',
        'executable              = {}singleJob.sh'.format(jobDir),
        'output                  = {}/logs/$(Process).out'.format(jobDir),
        'error                   = {}/logs/$(Process).err'.format(jobDir),
        'log                     = {}/logs/log.log'.format(jobDir),
        '+JobFlavour             = "workday"',
        # f'x509userproxy = /afs/cern.ch/user/{proxyDir}/.x509up_u120824',
        f'x509userproxy = /afs/cern.ch/user/{proxyDir}/.x509up_117245',
        'use_x509userproxy = True',
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
