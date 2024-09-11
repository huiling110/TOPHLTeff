import subprocess
import os
import re


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
    elif '2024C' in inputDir:
        era = '2024C'
    elif '2024D' in inputDir:
        era = '2024D'
    elif '2024E' in inputDir:
        era = '2024E'
    return era    

def getEraNano(url):
    match = re.search(r'Run(\d{4}[A-Z])', url)

    if match:
        era_string = match.group(1)
        return era_string
    else:
        print("Era string not found")

def extract_era_from_path(path):
    """
    Extracts the era pattern (e.g., "2024F") from the given directory path.

    Args:
    path (str): The directory path from which to extract the era pattern.

    Returns:
    str: The extracted era pattern, or None if no pattern is found.
    """
    # Regular expression pattern for the era, e.g., "2024F"
    pattern = re.compile(r'\b\d{4}[A-Z]\b')
    
    # Search for the pattern in the path
    match = pattern.search(path)
    
    if match:
        return match.group()
    return None    
   
 

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
    
def process_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your script.')
 
    # input = '/store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root'
    # input = '/store/data/Run2022C/Muon/NANOAOD/PromptNanoAODv10-v1/40000/d4484006-7e4b-424e-86a4-346d17d862f8.root'
    # input = '/store/data/Run2024E/Muon0/NANOAOD/PromptReco-v1/000/380/956/00000/8413549d-588b-46ff-9c53-b98b34faa7e7.root'
    input = '/store/data/Run2024D/Muon0/NANOAOD/PromptReco-v1/000/380/346/00000/3c839fb5-92c1-4140-a9ab-1efe2ad80a60.root'
    # input = '/store/data/Run2024C/Muon1/NANOAOD/PromptReco-v1/000/380/195/00000/0567ac8a-b6c6-466e-b0da-0474f2bbeea6.root'
    # Add arguments
    # parser.add_argument('--arg1', type=str, default='root://cmsxrootd.fnal.gov//'+input)
    parser.add_argument('--arg1', type=str, default=input)
    parser.add_argument('--arg2', type=str, default='./output/')
    parser.add_argument('--arg3', type=bool, default=True)
    parser.add_argument('--arg4', type=bool, default=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    arg1 = args.arg1
    arg2 = args.arg2
    arg3 = args.arg3
    arg4 = args.arg4

    # Return the arguments as a dictionary or use them directly in your function
    arguments = {
        'arg1': arg1,
        'arg2': arg2,
        'arg3': arg3,
        'arg4': arg4
    }

    return arguments
    
    