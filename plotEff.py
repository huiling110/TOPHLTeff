import os
import ROOT
import plotHelper as ph
import usefulFunc as uf


def main():
    
    
    # inputFile = '/afs/cern.ch/work/h/hhua/HLT_QDM/CMSSW_12_4_0_pre1/src/HLT-DQM-HTCondor/hua/output/eff.root'
    # inputFile = '/eos/user/h/hhua/forTopHLT/v0Hardronic2023C/result/eff.root'
    # inputFile2022 = '/eos/user/h/hhua/forTopHLT/v0Hardronic2022G/result/eff.root'
    # inputFile = '/eos/user/h/hhua/forTopHLT/v0Lep2023C/result/eff.root'
    # inputFile2022 = '/eos/user/h/hhua/forTopHLT/v0Lep2022G/result/eff.root'
    in2023B = '/eos/user/h/hhua/forTopHLT/2023B/v1ForHardronic/result/eff.root' 
    in2023C = '/eos/user/h/hhua/forTopHLT/2023C/v1ForHardronic/result/eff.root' 
    in2023D = '/eos/user/h/hhua/forTopHLT/2023D/v1ForHardronic/result/eff.root' 
    
    # eff_2023C = getEff(inputFile, 'de_2btag_jet_1pt', 'nu_2btag_jet_1pt')
    # eff_2023C = getEff(inputFile, 'de_2btag_jet_1pt', 'nu_2btag_jet_1pt')
    # eff_2023C = getEff(inputFile, 'de_eleJet_ele_1pt', 'nu_eleJet_ele_1pt')
    # eff_2022G = getEff(inputFile2022, 'de_eleJet_ele_1pt', 'nu_eleJet_ele_1pt')
    # eff_2023C = getEff(inputFile, 'de_eleHT_ele_1pt', 'nu_eleHT_ele_1pt')
    # eff_2022G = getEff(inputFile2022, 'de_eleHT_ele_1pt', 'nu_eleHT_ele_1pt')
    # eff_2023C = getEff(inputFile, 'de_2btag_jet_1pt', 'nu_1btag_jet_1pt')
    # eff_2022G = getEff(inputFile2022, 'de_2btag_jet_1pt', 'nu_1btag_jet_1pt')
    # eff_2023C = getEff(inputFile, 'de_2btag_jet_1pt', 'nu_2btag_jet_1pt')
    # eff_2022G = getEff(inputFile2022, 'de_2btag_jet_1pt', 'nu_2btag_jet_1pt')
   
    # outDir = getOutDir(inputFile) 
    # plotOverLay(eff_2022G, eff_2023C, outDir, 'leading jet pt')
    
    # era = uf.getEra(in2023B)
    
    eff_2023B = ph.getEffFromFile(in2023B, ['de_jetNum', 'nu_jetNum_1btag'])
    eff_2023C = ph.getEffFromFile(in2023C, ['de_jetNum', 'nu_jetNum_1btag'])
    eff_2023D = ph.getEffFromFile(in2023D, ['de_jetNum', 'nu_jetNum_1btag'])
    
    histList = [eff_2023B, eff_2023C, eff_2023D]
    legendList = ['2023B', '2023C', '2023D']
    outDir = getOutDir(in2023B) 
    plotName = outDir + 'HLTEff_jetNum_1btag.png'
    ph.plotOverlay(histList, legendList, '2023', 'HLT efficiency', plotName, [0, 1.])
   

 
def plotOverLay(h_2022, h_2023, outDir, axis = 'leading electron pt'):
    can = ROOT.TCanvas('efficiency', 'efficiency', 800, 800)
    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gStyle.SetOptTitle(0) 
   
    h_2022.SetLineWidth(4)
    h_2023.SetLineWidth(4)
    h_2022.SetLineColor(ROOT.kRed)
    h_2023.SetLineColor(ROOT.kBlue)
    
    h_2022.GetYaxis().SetTitle('Efficiency')
    h_2022.GetYaxis().SetTitleSize(0.04)
    # h_2022.GetYaxis().SetLabelSize(0.03)
    h_2022.GetYaxis().SetTitleOffset(1.0) 
    h_2022.GetXaxis().SetTitleOffset(0.9) 
    h_2022.GetXaxis().SetTitleSize(0.05)
    h_2022.GetXaxis().SetTitle(axis)
    
    h_2022.Draw()
    h_2023.Draw('same')
    
    # print('plot saved here: ', )
     
    legend = ROOT.TLegend(0.5,0.75,0.9,0.9)
    legend.AddEntry(h_2023, '2023C')
    legend.AddEntry(h_2022, '2022G')
    legend.Draw()
   
    addCMSTextToCan(can, 0.2, 0.35, 0.92)
     
    can.SaveAs(outDir + h_2023.GetName()+ '2023Cvs2022G.png')

    
   
def addCMSTextToCan(canvas, x1=0.23, x2=0.35, y=0.96, era = '2016'):
    can = canvas
     
    cmsTextFont = 61
    extraTextFont = 52
    cmsText = "CMS"
    extraText = "Preliminary"
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(31)
    latex.SetTextSize(0.04)
    latex.SetTextFont(cmsTextFont)
    latex.DrawLatex(x1, y, cmsText )
    latex.SetTextFont(extraTextFont)
    latex.SetTextSize(0.04*0.76)
    latex.DrawLatex(x2, y , extraText )
  
    # lumiText = lumiMap[era] /1000
    # lumiText_s = '{0:.1f}'.format(lumiText)
    # lumiText_s = str(lumiText)
    # lumiText_s = lumiText_s + ' fb^{-1}(13TeV)'
    lumiText_s = '(13.6TeV)'
    # print(lumiText)
    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.04)
    latex2.SetTextAlign(31)
    latex2.SetTextFont(42)  
    # latex2.DrawLatex(x2+0.6, y, lumiText_s )
    latex2.DrawLatex(x2+0.56, y, lumiText_s )
    

 
   
    
def getOutDir(inputFile):
    inputDir = inputFile.rsplit('/', 1)[0] +'/'
    outDir = inputDir+'results/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return outDir
     
    

def getEff(inputFile, deName, nuName):
    inputDir = inputFile.rsplit('/', 1)[0] +'/'
    inRoot = ROOT.TFile(inputFile, 'READ')
    
    outDir = inputDir+'results/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    
    de = inRoot.Get(deName) 
    nu = inRoot.Get(nuName)
    eff = de.Clone()
    eff.Reset()
    eff.Sumw2()
    eff.Divide( nu, de)
    eff.Print() 
    
    can = ROOT.TCanvas('efficiency', 'efficiency', 800, 800)
    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gStyle.SetOptTitle(0) 
    
    eff.Draw()
    eff.SetDirectory(0)

    can.SaveAs(inputDir+ nuName +'_eff.png')
    inRoot.Close()
    
    return eff
        
    
if __name__=='__main__':
    main() 
    
