import subprocess

def main():
    #dasgoclient --query="dataset=/Muon*/Run2023*-PromptNanoAODv*/NANOAOD"  for getting datasets
    datasets = [
    # '/Muon0/Run2023B-PromptNanoAODv11p9_v1-v2/NANOAOD',
    # '/Muon1/Run2023B-PromptNanoAODv11p9_v1-v2/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv11p9_v1-v1/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv11p9_v1-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD',
    # '/Muon0/Run2023D-PromptReco-v1/NANOAOD',
    # '/Muon0/Run2023D-PromptReco-v2/NANOAOD',
    # '/Muon1/Run2023D-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2023D-PromptReco-v2/NANOAOD ',
   
    # '/Muon/Run2022C-PromptNanoAODv10-v1/NANOAOD',
    # '/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD',
    # '/Muon/Run2022D-PromptNanoAODv10_v1-v1/NANOAOD',
    # '/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD',
    # '/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD',
    # '/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD',
    # '/Muon/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD',
    # '/Muon/Run2022G-PromptNanoAODv10_v1-v1/NANOAOD',
    # '/Muon/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD',

    # '/Muon0/Run2024C-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024C-PromptReco-v1/NANOAOD',    

    # '/Muon0/Run2024D-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024D-PromptReco-v1/NANOAOD',
    # '/Muon0/Run2024E-PromptReco-v1/NANOAOD',
    # '/Muon0/Run2024E-PromptReco-v2/NANOAOD'
    # '/Muon1/Run2024E-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024E-PromptReco-v2/NANOAOD',
    
    # '/Muon0/Run2024F-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024F-PromptReco-v1/NANOAOD',
    
    #!2024G, not complete yet
    # '/Muon0/Run2024G-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024G-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024H-PromptReco-v1/NANOAOD',
    # '/Muon0/Run2024H-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024I-PromptReco-v1/NANOAOD',
    # '/Muon0/Run2024I-PromptReco-v1/NANOAOD',
    # '/Muon1/Run2024I-PromptReco-v2/NANOAOD',
    # '/Muon0/Run2024I-PromptReco-v2/NANOAOD',
    
    # '/EGamma1/Run2024F-PromptReco-v1/NANOAOD',
    # '/EGamma0/Run2024F-PromptReco-v1/NANOAOD',
    # '/EGamma1/Run2024G-PromptReco-v1/NANOAOD',
    # '/EGamma0/Run2024G-PromptReco-v1/NANOAOD',
    
# /EGamma1/Run2024G-PromptReco-v1/NANOAOD
    ]
    
    # outList = 'Muon2023B'
    # outList = 'Muon2023C'
    # outList = 'Muon2023D'
    # outList = 'Muon2022'
    # outList = 'Muon2024C'
    # outList = 'Muon2024D'
    # outList = 'Muon2024D_all'
    # outList = 'Muon2024E'
    # outList = 'Muon2024F'
    # outList = 'Muon2024G_partial'
    # outList = 'EGamma2024F'
    # outList = 'EGamma2024G_partial'
    # outList = 'Muon2024G'
    # outList = 'Muon2024H'
    # outList = 'Muon2024I'
  
  
  
   
    filesList = [] 
    for idataset in datasets: 
        iList = getFiles(idataset)
        filesList.extend(iList)
    print(filesList)
    
    
    outList = 'input/' + outList +'.txt'
    print(outList)
    saveListToTxt(filesList, outList)
    
def saveListToTxt(inList, outFile):
    with open(outFile, 'w') as file:
    # Loop through the list and write each element to a separate line
        for item in inList:
            file.write("%s\n" % item)    
    print('file saved here: ', outFile)
    
def getFiles(dataset):
    command = 'dasgoclient --query=\"file dataset={}\"'.format( dataset)   
    print('run command: ', command)
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(output.stdout)
    lists = output.stdout.splitlines()
    # print(lists)
    return lists
    
    
    
if __name__=='__main__':
    main()
