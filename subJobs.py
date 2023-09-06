import os

def main():
    inputList = 'input/Muon2023B.txt'
    
    inName = getListFromTxt(inputList)
    print(inName)
   
    jobDir = getNameFromPath(inputList)
    
    for iList in inList:
        writeJob(iList, jobName)
   
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
def getNameFromPath(inPath):
    base_file_name = os.path.basename(file_path)
    # Remove the '.txt' postfix
    file_name_without_extension = os.path.splitext(base_file_name)[0]
    return file_name_without_extension
    

def writeJob(inFile):
        
    
   
def subSingleJob():
    command = 'condor_submit hello.sub'  
    
    
if __name__=='__main__':
    main() 