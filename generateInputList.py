import subprocess

def main():
    #dasgoclient --query="dataset=/Muon*/Run2023*-PromptNanoAODv*/NANOAOD"  for getting datasets
    datasets = [
    '/Muon0/Run2023B-PromptNanoAODv11p9_v1-v2/NANOAOD',
    '/Muon1/Run2023B-PromptNanoAODv11p9_v1-v2/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv11p9_v1-v1/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD',
    # '/Muon0/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv11p9_v1-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD',
    # '/Muon1/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD',
    ]
    
    outList = 'Muon2023B'
   
    filesList = [] 
    for idataset in datasets: 
        iList = getFiles(idataset)
        filesList.extend(iList)
    print(filesList)
    
    
    outList = 'input/' + outList +'.txt'
    print(outList)
    
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