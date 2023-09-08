import numpy as np
import os
import ROOT

import skimNano as sn
import usefulFunc as uf

def main():
    # isTest = True
    isTest =False
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Hardronic2023C/' 
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Hardronic2022G/' 
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Lep2023C/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Lep2022G/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/v1ForHardronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2023B/v1ForHardronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2023C/v1ForHardronic/'
    inputDir = '/eos/user/h/hhua/forTopHLT/2023D/v1ForHardronic/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/2022/v1ForHardronic/'
    isHadronic = True
    # isHadronic = False
   
    era = uf.getEra(inputDir) 
   
    outFile = makeOutFile(inputDir, isTest) 
    
    print('inputDir: ', inputDir)
    chain = ROOT.TChain('Events')
    chain.Add(inputDir+'*.root')
    # chain.Add(inputDir+'e61eefa9-42c0-4d5d-9d6a-93258ede52ec.root')
    entries = chain.GetEntries()
    print('entries: ', entries)
  
    if isHadronic:
        histList = makeHist_hard(chain, isTest, era) 
    else:
        histList = makeHist_ele(chain, isTest)
  
   
    for ih in histList:
        ih.Print()
        ih.SetDirectory(outFile)
    
    print('outFile here: ', outFile.GetName())
    outFile.Write()
    outFile.Close()

def makeHist_ele(chain, isTest):
    binning_e = np.array((0.,25.,30.,32.5,35.,40.,45.,50.,60.,80.,120.,200.,400.))
    de_eleJet = ROOT.TH1D('de_eleJet_ele_1pt', 'de_eleJet_ele_1pt', len(binning_e)-1,binning_e)
    nu_eleJet = ROOT.TH1D('nu_eleJet_ele_1pt', 'nu_eleJet_ele_1pt', len(binning_e)-1,binning_e)
    de_eleHT = ROOT.TH1D('de_eleHT_ele_1pt', 'de_eleHT_ele_1pt', len(binning_e)-1,binning_e)
    nu_eleHT = ROOT.TH1D('nu_eleHT_ele_1pt', 'nu_eleHT_ele_1pt', len(binning_e)-1,binning_e)
    
    entries = chain.GetEntries()
    if isTest:
        entries = 10000
    for entry in range(entries):
        chain.GetEntry(entry)
        nj_ele, HT = sn.jetSel(chain) 
        ne = sn.getEleNum(chain)
        if((nj_ele > 0) & (ne>0)):
            de_eleJet.Fill(chain.Electron_pt[0])
            if(chain.HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned==1):
                nu_eleJet.Fill(chain.Electron_pt[0])
        
        if((nj_ele > 1) & (ne>0) & (HT>100.) ):
            de_eleHT.Fill(chain.Electron_pt[0])
            if(chain.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1):
                nu_eleHT.Fill(chain.Electron_pt[0])
    histList = [de_eleHT, nu_eleHT, de_eleJet, nu_eleJet]
    return histList    
    

def makeHist_hard(chain, isTest, era):
    #!!!should switch to TEfficiency for efficiency calculation
    de_jetNum = ROOT.TH1D('de_jetNum', 'n^{jet}', 6, 6, 12)
    nu_jetNum_1btag =  ROOT.TH1D('nu_jetNum_1btag', 'n^{jet}', 6, 6, 12)
    nu_jetNum_2btag = ROOT.TH1D('nu_jetNum_2btag', 'n^{jet}', 6, 6, 12)
    nu_jetNum_both = ROOT.TH1D('nu_jetNum_both', 'n^{jet}', 6, 6, 12)
    
    de_bjetNum = ROOT.TH1D('de_bjetNum', 'n^{b-jet}', 5, 1.5, 6.5)
    nu_bjetNum_1btag =  ROOT.TH1D('nu_bjetNum_1btag', 'n^{b-jet}', 5, 1.5, 6.5)
    nu_bjetNum_2btag = ROOT.TH1D('nu_bjetNum_2btag', 'n^{b-jet}', 5, 1.5, 6.5)
    nu_bjetNum_both = ROOT.TH1D('nu_bjetNum_both', 'n^{b-jet}', 5, 1.5, 6.5)
    
    binning = np.array((500., 550., 600., 650., 700., 800., 900., 1000., 1300., 2000)) 
    de_HT = ROOT.TH1D('de_HT', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_1btag =  ROOT.TH1D('nu_HT_1btag', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_2btag = ROOT.TH1D('nu_HT_2btag', 'HT(GeV)', len(binning)-1, binning)
    nu_HT_both = ROOT.TH1D('nu_HT_both', 'HT(GeV)', len(binning)-1, binning)
    
    entries = chain.GetEntries()
    if isTest:
        entries = 10000
    for entry in range(entries):
        chain.GetEntry(entry)
        
        #!!!change to era dependant
        if era =='2023C' or era =='2023B' or era=='2022':
            HLT_1btag = chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59
            HLT_2btag = chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94 
            btag = 0
        else: 
            HLT_1btag = chain.HLT_PFHT450_SixPFJet36_PNetBTag0p35
            HLT_2btag = chain.HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50
            btag =1
        
    #preslection
        jetNum, HT = jetSel(chain)
        bjetNum, bHT = jetSel(chain, True, btag)
        if ( not (jetNum>5 and HT>500 and bjetNum>1)):
            continue
        
        de_jetNum.Fill(jetNum)
        de_HT.Fill(HT)
        de_bjetNum.Fill(bjetNum)
      
            
            
            
        if HLT_1btag:
            nu_jetNum_1btag.Fill(jetNum)
            nu_bjetNum_1btag.Fill(bjetNum)
            nu_HT_1btag.Fill(HT)
        if HLT_2btag:
            nu_jetNum_2btag.Fill(jetNum)
            nu_bjetNum_2btag.Fill(bjetNum)
            nu_HT_2btag.Fill(HT)
        if HLT_2btag or HLT_1btag:
            nu_jetNum_both.Fill(jetNum)
            nu_bjetNum_both.Fill(bjetNum)
            nu_HT_both.Fill(HT)
            
            
    histList = [de_jetNum, nu_jetNum_1btag, nu_jetNum_2btag, nu_jetNum_both, de_bjetNum, nu_bjetNum_1btag, nu_bjetNum_2btag, nu_bjetNum_both, de_HT, nu_HT_1btag, nu_HT_2btag, nu_HT_both]
    return histList
        
    
    
def makeOutFile(inputDir, isTest):
    outDir = inputDir+ 'result/'
    if isTest:
        outDir = 'output/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    outFile = ROOT.TFile(outDir+'eff.root', 'RECREATE')
    return outFile
    
      
def preSel( chain) :
    # for Jet in range(0,chain.nJet):
    #     if abs(chain.Jet_eta[Jet])>2.4: 
    #         continue
    #     if chain.Jet_pt[Jet]<30: 
    #         continue
    #     # chain ht
    #     if((chain.Jet_pt[Jet] > 30.) & (abs(chain.Jet_eta[Jet])<2.4)): 
    #         ht = ht + chain.Jet_pt[Jet]
    #     # nJets
    #     if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) ):
    #         nj = nj+1
    #     # nbJets
    #     if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagDeepFlavB[Jet]>0.2770)):
    #         nb = nb+1
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagdeepb[Jet]>0.4941)):##!!!
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagPNetB[Jet]>0.4941)):##!!!
        
    jetNum, HT = jetSel(chain)
    bjetNum, bHT = jetSel(chain, True)
        
    # ifPass = (nj > 5)  & (nb>1) & (ht>500) & (chain.HLT_IsoMu27==1)
    # ifPass = jetNum>5 and HT>500 and bjetNum>1 and chain.HLT_IsoMu27==1
    ifPass = jetNum>5 and HT>500 and bjetNum>0 and chain.HLT_IsoMu27==1
    return ifPass

def jetSel(chain, isB=False, btag=0):
    jetNum = 0
    HT = 0
    for i in range(0, chain.nJet):
        if( not (chain.Jet_pt[i] > 30.) and (abs(chain.Jet_eta[i])<2.4)) :
            continue
        if isB:
            # DeepJet 0.351; PNet: 0.387
        #!!!change to era dependant
            if btag == 0:
                if( not (chain.Jet_btagDeepFlavB[i]>0.351)):
                    continue
            if btag==1:
                if( not (chain.Jet_btagPNetB[i]>0.351)):
                    continue
                
        jetNum+=1
        HT = HT+ chain.Jet_pt[i] 
        # print(HT, chain.Jet_pt[i])
    return jetNum, HT 
    
           
    

if __name__=='__main__':
    t = ROOT.TStopwatch()
    t.Start()
    main()
    t.Stop()
    t.Print()