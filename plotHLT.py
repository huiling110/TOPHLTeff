import ROOT
import numpy as np
import os

import skimNano as sn

def main():
    # isTest = True
    isTest =False
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Hardronic2023C/' 
    inputDir = '/eos/user/h/hhua/forTopHLT/v0Hardronic2022G/' 
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Lep2023C/'
    # inputDir = '/eos/user/h/hhua/forTopHLT/v0Lep2022G/'
    isHadronic = True
    # isHadronic = False
   
    outFile = makeOutFile(inputDir, isTest) 
    
    print('inputDir: ', inputDir)
    chain = ROOT.TChain('Events')
    chain.Add(inputDir+'*.root')
    # chain.Add(inputDir+'e61eefa9-42c0-4d5d-9d6a-93258ede52ec.root')
    entries = chain.GetEntries()
    print('entries: ', entries)
  
    if isHadronic:
        histList = makeHist_hard(chain, isTest) 
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
    

def makeHist_hard(chain, isTest):
    binning =  np.array((0.,5.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,60.,65.,70.,75.,80.,90.,100.,120.,140.,160.,200.))
    h_de = ROOT.TH1D('de_2btag_jet_1pt', 'de_2btag_jet_1pt', len(binning)-1,binning)
    h_nu = ROOT.TH1D('nu_2btag_jet_1pt', 'nu_2btag_jet_1pt', len(binning)-1,binning)
    h_nu_1btag = ROOT.TH1D('nu_1btag_jet_1pt', 'nu_1btag_jet_1pt', len(binning)-1,binning)
    
    #preslection
    entries = chain.GetEntries()
    if isTest:
        entries = 10000
    for entry in range(entries):
        chain.GetEntry(entry)
        
        ifPre = preSel(chain)
        if not ifPre:
            continue
        h_de.Fill(chain.Jet_pt[0])
        
        if chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94==1:
            h_nu.Fill(chain.Jet_pt[0]) 
        if chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59==1:
            h_nu_1btag.Fill(chain.Jet_pt[0])
    histList = [h_de, h_nu, h_nu_1btag]
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
    ht=0
    nj=0
    nb=0
    for Jet in range(0,chain.nJet):
        if abs(chain.Jet_eta[Jet])>2.4: 
            continue
        if chain.Jet_pt[Jet]<30: 
            continue
        # chain ht
        if((chain.Jet_pt[Jet] > 30.) & (abs(chain.Jet_eta[Jet])<2.4)): 
            ht = ht + chain.Jet_pt[Jet]
        # nJets
        if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) ):
            nj = nj+1
        # nbJets
        if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagDeepFlavB[Jet]>0.2770)):
            nb = nb+1
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagdeepb[Jet]>0.4941)):##!!!
        # if((chain.Jet_pt[Jet] > 40.) & (abs(chain.Jet_eta[Jet])<2.4) & (chain.Jet_btagPNetB[Jet]>0.4941)):##!!!
        
    ifPass = (nj > 5)  & (nb>1) & (ht>500) & (chain.HLT_IsoMu27==1)
    return ifPass


           
    

if __name__=='__main__':
    t = ROOT.TStopwatch()
    t.Start()
    main()
    t.Stop()
    t.Print()