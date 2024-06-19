import ROOT
import os
import argparse

import usefulFunc as uf

triggerSwitchedMap = {
    '2024C': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5',
    '2024D': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
    '2024E': 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3',
} 

# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v4-v1/60000/fdd8324d-a4f8-4286-945f-5528e7ae46e9.root', version = 'v0ForHadronic', ifForHadronic = True,   ifTest = False):
# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023D/Muon0/NANOAOD/PromptReco-v1/000/369/901/00000/3bdb0fca-4c12-4394-9812-509cb1d05cb7.root', version = 'v0ForHadronic', ifForHadronic = True,   ifTest = True):
# def main(inputNano = 'root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v1/70000/61280236-03a6-4cf3-8008-6eca1d7236d0.root', version = 'v0ForHadronic', ifForHadronic = True,   ifTest = True):
def main(inputNano = 'root://cmsxrootd.fnal.gov///store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root', outDir = './output/', ifForHadronic = True,   ifTest = True):
    # inputNano = 'root://cmsxrootd.fnal.gov/' +'/store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v3-v1/2820000/e55c38a4-5776-4b0f-8190-39da36d63bca.root' 


    inputNano = 'root://cmsxrootd.fnal.gov/'+ inputNano
    
    
    
    preSel(inputNano,  outDir, ifForHadronic, ifTest)#faster run time with rDataFrame
    
    # selLoop(chain, branches_to_keep, outDir, ifForHadronic, ifTest)#!obsolete, keep it for now
    
def preSel(inputNano,  outDir, ifForHadronic, ifTest):
    #faster and better with rDataFrame:)
    ROOT.gInterpreter.Declare("""
    #include <vector>
    #include "Math/Vector4D.h"
        auto jetSelNew = [](const ROOT::VecOps::RVec<float>& Jet_pt, const ROOT::VecOps::RVec<float>& Jet_eta, 
                    const ROOT::VecOps::RVec<float>& Jet_phi, const ROOT::VecOps::RVec<float>& Jet_mass, const ROOT::VecOps::RVec<float>& Jet_btagPNetB, Bool_t isB=kFALSE) { 
            std::vector<ROOT::Math::PtEtaPhiMVector> selectedJets;
            for (int i = 0; i < Jet_pt.size(); i++) {
                if (!(Jet_pt[i] > 25. && abs(Jet_eta[i]) < 2.4)) continue;
                if (isB) {
                    if (!(Jet_btagPNetB[i] > 0.387)) continue;
                } 
                selectedJets.emplace_back(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
            }
            return selectedJets;
        };
    """) 
    
    ROOT.gInterpreter.Declare("""
    auto HTCal = [](const std::vector<ROOT::Math::PtEtaPhiMVector>& jets) {
        double ht = 0.0;
        for (const auto& jet : jets) {
            ht += jet.Pt();
        }
        return ht;
    };
    """)
    
    print('input: ', inputNano) 
    df = ROOT.RDataFrame("Events", inputNano)
    # print(df.GetColumnNames())  
    print('initial events: ', df.Count().GetValue())
    if ifTest:
        df = df.Range(10000)
   
    df = df.Filter('HLT_IsoMu24==1')
    
    df = df.Define('selectedJets', 'jetSelNew(Jet_pt, Jet_eta, Jet_phi, Jet_mass,  Jet_btagPNetB, kFALSE )')
    df = df.Define('selectedBjets', 'jetSelNew(Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_btagPNetB, kTRUE )')
    df = df.Define('nj', '(int)selectedJets.size()')
    df = df.Define('nb', '(int)selectedBjets.size()')
    # df = df.Define('HT', 'std::accumulate(selectedJets.begin(), selectedJets.end(), 0., [](double sum, const ROOT::Math::PtEtaPhiMVector& jet) { return sum + jet.Pt(); })')
    df = df.Define('jet_6pt', 'nj>5 ? selectedJets[5].Pt() : -1')
    df = df.Define("HT", "HTCal(selectedJets)")

    
    preSelect = 'nj>5 && HT>500. && nb>1'
    df = df.Filter(preSelect)
    
    
    if ifTest:
        outDir = './output/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    era = uf.getEra(inputNano)
       
    # List of branch names to keep
    branches_to_keep = [
                        #2023D
                        'HLT_PFHT450_SixPFJet36_PNetBTag0p35',
                        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50',
                        triggerSwitchedMap[era],
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5', # ![ 378981, 380933], from HLT INFO GUI
                        # 'HLT_PFHT340_QuadPFJet70_50_40_40_PNet2BTagMean0p70', #3.2	[378981,380933] ; 2024C[37941, 380252]
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3', ##!seems not available in 2024C, starting 379613
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',#!prescaled!
                        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55',#!ParkingHH since 2023C run 367661
                        'HLT_IsoMu24',
                        # 'HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned',# !disabled in 2024
                        # 'HLT_Ele28_eta2p1_WPTight_Gsf_HT150', #!disabled in 2024
                        'HLT_Ele30_WPTight_Gsf',
                        # 'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53', #!added in 2024C after run 379613
                        # 'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53',#!added in 2024C after run 379613
                        "run",
                        ]
        
    branches_to_keep.append('nj')
    branches_to_keep.append('nb')    
    branches_to_keep.append('HT')
    branches_to_keep.append('jet_6pt')
    postFix = inputNano.rsplit("/", 1)[-1]
    df.Snapshot("Events", outDir+postFix, branches_to_keep)
    print('after selection: ', df.Count().GetValue())
    print('file saved here: ', outDir+postFix)
   
   
   
   
    
    
def selLoop(chain, branches_to_keep, outDir, ifForHadronic, ifTest):
    # List of branch names to keep
    branches_to_keep = [
                        # 'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
                        # 'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
                        # 2023B and 2023C and 2022B
                        # 'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94',#disabled
                        # 'HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59',#disabled
                        #2023D
                        'HLT_PFHT450_SixPFJet36_PNetBTag0p35',
                        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50',
                        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3', #!seems not available in 2024C
                        # 'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',#!prescaled!
                        #Additional triggers for DeepJet vs ParticleNet comparison
                        # 'HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65',
                        # 'HLT_QuadPFJet70_50_40_35_PNet2BTagMean0p65',
                        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55',#!ParkingHH since 2023C run 367661
                        
                        'HLT_IsoMu24',
                        'HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned',
                        'HLT_Ele28_eta2p1_WPTight_Gsf_HT150',
                        'HLT_Ele30_WPTight_Gsf',
                        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53', #!added in 2024C after run 379613
                        'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53',#!added in 2024C after run 379613
                        "run",
                        "nJet", 
                        'Jet_pt',
                        'Jet_eta',
                        'Jet_phi',
                        'Jet_jetId', #? why all 0?
                        'Jet_btagDeepFlavB', 
                        'Jet_btagPNetB', #2023D
                        'nElectron',
                        'Electron_pt',
                        'Electron_eta',
                        'Electron_phi',
                        'Electron_cutBased',
                        'PV_npvs',
                        'PV_npvsGood'
                        ]
    chain = ROOT.TChain("Events")
    chain.AddFile(inputNano)
    print('input: ', inputNano)
    
    print('entries in old tree: ', chain.GetEntries())
   
    print('ifTest=', ifTest, '  ifForHadronic=', ifForHadronic) 

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
        if not (chain.HLT_IsoMu24==1): #!!!add muon selection here
            continue
        if ifForHadronic:
            nj, HT=jetSel(chain)
            if not (nj>5 and HT>400):
                continue 
        else:
            eleNum = getEleNum(chain)
            if not (chain.HLT_IsoMu24==1 and eleNum>=1 ):
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
        #if((chain.Electron_pt[electron] > 25.) & (abs(chain.Electron_eta[electron])<2.1) & (chain.Electron_cutBased[electron]>=4) & ((chain.Electron_eta[electron]<-1.8) or (chain.Electron_eta[electron]>0.6)) & ((chain.Electron_phi[electron]>-0.5) or (chain.Electron_phi[electron]<-1.5))): #For checking BPix issue in Run 2023D
        # if((chain.Electron_pt[electron] > 25.) & (abs(chain.Electron_eta[electron])<2.1) & (chain.Electron_cutBased[electron]>=4) & (chain.run<367765)): #For checking HCAL scale update in Run 2023C
            ne = ne+1
    return ne

#https://cms-nanoaod-integration.web.cern.ch/autoDoc/NanoAODv14/2024Prompt/doc_EGamma1_Run2024D-PromptReco-v1.html#Jet
def jetSel(chain):
    jetNum=0
    HT = 0
    for Jet in range(0,chain.nJet):
        # if((chain.Jet_pt[Jet] > 30.) and (abs(chain.Jet_eta[Jet])<2.4) and chain.Jet_jetId[Jet]>0):
        # if((chain.Jet_pt[Jet] > 40.) and (abs(chain.Jet_eta[Jet])<2.4)) :
        # if((chain.Jet_pt[Jet] > 40.) and (abs(chain.Jet_eta[Jet])<2.4) and ((chain.Jet_eta[Jet]<-1.8) or (chain.Jet_eta[Jet]>0.6)) and ((chain.Jet_phi[Jet]>-0.5) or (chain.Jet_phi[Jet]<-1.5))) : #For checking BPix issue in Run 2023D
        # if((chain.Jet_pt[Jet] > 40.) and (abs(chain.Jet_eta[Jet])<2.4) and (chain.run<367765)) : #For checking HCAL scale update in Run 2023C
        # if((chain.Jet_pt[Jet] > 40.) and (abs(chain.Jet_eta[Jet])<2.4) and (chain.run <= 380649) and (chain.run >= 380647)) : #For checking HCAL calib update in Run 2024D (fill 9618 postcalib)
        # if((chain.Jet_pt[Jet] > 40.) and (abs(chain.Jet_eta[Jet])<2.4) and (chain.run <= 380626) and (chain.run >= 380564)) : #For checking HCAL calib update in Run 2024D (fill 9611 + 9614 precalib)
        # print(chain.Jet_pt[Jet], chain.Jet_eta[Jet], chain.Jet_jetId[Jet])
        # if(chain.Jet_pt[Jet] > 25. and abs(chain.Jet_eta[Jet])<2.4 and chain.Jet_jetId[Jet]& (1 << 2)!=0):# tight jetID, recommendation from JETPOG for 2022
        if(chain.Jet_pt[Jet] > 25. and abs(chain.Jet_eta[Jet])<2.4):# !seems Jet_jetId is all 0
            jetNum+=1
            HT=HT+chain.Jet_pt[Jet] 
    return jetNum, HT    

def process_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your script.')
 
    # input = '/store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/60000/06d25571-df3e-4ceb-9e44-7452add3e004.root'
    # input = '/store/data/Run2022C/Muon/NANOAOD/PromptNanoAODv10-v1/40000/d4484006-7e4b-424e-86a4-346d17d862f8.root'
    # input = '/store/data/Run2024E/Muon0/NANOAOD/PromptReco-v1/000/380/956/00000/8413549d-588b-46ff-9c53-b98b34faa7e7.root'
    # input = '/store/data/Run2024D/Muon0/NANOAOD/PromptReco-v1/000/380/346/00000/3c839fb5-92c1-4140-a9ab-1efe2ad80a60.root'
    input = '/store/data/Run2024C/Muon1/NANOAOD/PromptReco-v1/000/380/195/00000/0567ac8a-b6c6-466e-b0da-0474f2bbeea6.root'
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


if __name__=='__main__':
    args = process_arguments()
    #!!!need to update so that test and subjob is easy
    # main(args['arg1'], args['arg2'], args['arg3'], args['arg4'])
    #main(args['arg1'], args['arg2'], False, False) #ele
    main(args['arg1'], args['arg2'], True, False) #hadronic
    # main(args['arg1'], args['arg2'], True, True) #test
    # main(args['arg1'], args['arg2'], False, True) #test
