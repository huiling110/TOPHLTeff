import ROOT
import os
import argparse


#!!!Maybe try rDataFrame in the future
# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v4-v1/60000/fdd8324d-a4f8-4286-945f-5528e7ae46e9.root', version = 'v0ForHadronic', ifForHardronic = True,   ifTest = False):
# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023D/Muon0/NANOAOD/PromptReco-v1/000/369/901/00000/3bdb0fca-4c12-4394-9812-509cb1d05cb7.root', version = 'v0ForHadronic', ifForHardronic = True,   ifTest = True):
# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v1/70000/61280236-03a6-4cf3-8008-6eca1d7236d0.root', version = 'v0ForHadronic', ifForHardronic = True,   ifTest = True):
def main(inputNano = 'root://cmsxrootd.fnal.gov///store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root', outDir = './output/', ifForHardronic = True,   ifTest = True):
    # inputNano = 'root://cmsxrootd.fnal.gov/' +'/store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v3-v1/2820000/e55c38a4-5776-4b0f-8190-39da36d63bca.root' 


    # input_file = ROOT.TFile(inputNano, "READ")  #???not sure TFile not working
    # input_tree = input_file.Get("Events")
    chain = ROOT.TChain("Events")
    chain.AddFile(inputNano)
    
    print('entries in old tree: ', chain.GetEntries())
   
    print('ifTest=', ifTest, '  ifForHardronic=', ifForHardronic) 

    # List of branch names to keep
    branches_to_keep = [
                        'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
                        'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
                        # 2023B and 2023C
                        'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94',
                        'HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59',
                        #2023D
                        'HLT_PFHT450_SixPFJet36_PNetBTag0p35',
                        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50',
                        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',
                        
                        "HLT_IsoMu27", 
                        'HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned',
                        'HLT_Ele28_eta2p1_WPTight_Gsf_HT150',
                        "run",
                        "nJet", 
                        'Jet_pt',
                        'Jet_eta',
                        'Jet_btagDeepFlavB', 
                        'Jet_btagPNetB', #2023D
                        'nElectron',
                        'Electron_pt',
                        'Electron_eta',
                        'Electron_cutBased'
                        ]

    chain.SetBranchStatus('*', 0)
    for branch_name in branches_to_keep:
        if chain.GetBranch(branch_name):
            chain.SetBranchStatus(branch_name, 1)  # Enable the desired branch
        else:
            print('branch not exist: ', branch_name, '!!!\n')
    output_tree = chain.CloneTree(0)  # have to be after the chain.SetBranchStatus
   
    entries = chain.GetEntries()
    if ifTest:
        entries =10000
    for entry in range(entries):
        chain.GetEntry(entry)
        if not (chain.HLT_IsoMu27==1): #!!!add muon selection here
            continue
        if ifForHardronic:
            nj, HT=jetSel(chain)
            if not (nj>5 and HT>400):
                continue 
        else:
            eleNum = getEleNum(chain)
            if not (chain.HLT_IsoMu27==1 and eleNum>=1 ):
                continue
                
        output_tree.Fill()
        
        
    # outDir = '/eos/user/h/hhua/forTopHLT/'
    # outDir = outDir+version+'/'
    if ifTest:
        outDir = './output/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    postFix = inputNano.rsplit("/", 1)[-1]
    output_file = ROOT.TFile(outDir+postFix, "RECREATE") 
    print('entries in new tree: ', output_tree.GetEntries())
    output_tree.SetDirectory(output_file)
    # output_file.Print()
    print('output file here: ', output_file.GetName())
    output_file.Write()
    output_file.Close()


def getEleNum(chain):
    ne = 0
    for electron in range(0,chain.nElectron):
        # nElectrons
        if((chain.Electron_pt[electron] > 25.) & (abs(chain.Electron_eta[electron])<2.1) & (chain.Electron_cutBased[electron]>=4)):
            ne = ne+1
    return ne

def jetSel(chain):
    jetNum=0
    HT = 0
    for Jet in range(0,chain.nJet):
        # if((chain.Jet_pt[Jet] > 30.) and (abs(chain.Jet_eta[Jet])<2.4) and chain.Jet_jetId[Jet]>0):
        if((chain.Jet_pt[Jet] > 30.) and (abs(chain.Jet_eta[Jet])<2.4)) :
            jetNum+=1
            HT=HT+chain.Jet_pt[Jet] 
    return jetNum, HT    

def process_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your script.')

    # Add arguments
    parser.add_argument('arg1', type=str, help='Description of argument 1.')
    parser.add_argument('arg2', type=str, help='Description of argument 2.')
    parser.add_argument('arg3', type=bool, help='Description of argument 2.')
    parser.add_argument('arg4', type=bool, help='Description of argument 2.')

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




if __name__=='__main__':
    args = process_arguments()
    # if len(argz)>0:
    main(args['arg1'], args['arg2'], True, False)
    # main(args['arg1'], args['arg2'], False, False)
    # else:
    # main()