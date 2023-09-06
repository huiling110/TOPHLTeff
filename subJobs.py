import os

import usefulFunc as uf

def main():
    inputList = 'input/Muon2023B.txt'
    jobVersion = 'v1ForHardronic'
    
    # inList = getListFromTxt(inputList)
    # print(inList)
   
    jobDir = getNameFromPath(inputList)
    jobDir = 'jobs/'+jobDir + '/'
    uf.checkMakeDir(jobDir)
    print(jobDir)
    
    # for i, iList in enumerate(inList):
    #     jobName = jobDir + i + '.sh'
    writeJob( jobDir+'singleJob.sh', inputList, jobVersion)
    
     
    # subAllJobs()  
  
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
    

def writeJob( jobName, inFile, jobVersion):
    lines = [
        '#!/bin/bash',
        'cd /afs/cern.ch/work/h/hhua/HLTStudy/TOPHLTeff/',
        'lines=(`cat /afs/cern.ch/work/h/hhua/HLTStudy/TOPHLTeff/{}`)'.format(inFile),
        'echo \$\{lines[\$1]\}',
        # 'python3 skimNano.py root://cmsxrootd.fnal.gov/$\{lines[\$1]\} {} 1 0'.format(jobVersion), 
        'python3 skimNano.py root://cmsxrootd.fnal.gov/$\{lines[$1]\} ' + '{} 1 0'.format(jobVersion),
    ]
    
    writeListToFile(lines, jobName)
        

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