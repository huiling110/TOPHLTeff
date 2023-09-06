

def main():
    inputList = 'input/Muon2023B.txt'
    
    inList = getListFromTxt(inputList)
    print(inList)
    
    # for iList in inList:
    #     writeJob(iList)
   
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
    
    
    
   
def subSingleJob():
    command = 'condor_submit hello.sub'  
    
    
if __name__=='__main__':
    main() 