
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