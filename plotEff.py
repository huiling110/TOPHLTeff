import os
import ROOT
import plotHelper as ph
import usefulFunc as uf


def main():
    # in2023B = '/eos/user/v/vshang/forTopHLT_11052023/2023B/v1ForHadronic/result/eff.root' 
    # in2023C = '/eos/user/v/vshang/forTopHLT_11052023/2023C/v1ForHadronic/result/eff.root' 
    # in2022 = '/eos/user/v/vshang/forTopHLT_11052023/2022/v1ForHadronic/result/eff.root'
    # in2023D = '/eos/user/v/vshang/forTopHLT_05072024/2023D/v1ForHadronic/result/eff.root'
    # in2024C = '/eos/user/v/vshang/forTopHLT_05072024/2024C/v1ForHadronic/result/eff.root'
    # in2023D = '/eos/user/v/vshang/forTopHLT_05072024/2024DpreCalib/v1ForHadronic/result/eff.root'
    # in2024C = '/eos/user/v/vshang/forTopHLT_05072024/2024DpostCalib/v1ForHadronic/result/eff.root'
    ifHadronic =True
    
    in2024D = '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/result/eff.root'
    in2024E = '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/result/eff.root'
    # in2023B = '/eos/user/v/vshang/forTopHLT_12192023BPix/2023B/v1ForEle/result/eff.root' 
    # in2023C = '/eos/user/v/vshang/forTopHLT_12192023BPix/2023C/v1ForEle/result/eff.root' 
    # in2023D = '/eos/user/v/vshang/forTopHLT_12192023BPix/2023D/v1ForEle/result/eff.root' 
    # in2022 = '/eos/user/v/vshang/forTopHLT_12192023BPix/2022/v1ForEle/result/eff.root'
    # in2023B = '/eos/user/v/vshang/forTopHLT_11052023/2023B/v1ForEle/result/eff.root' 
    # in2023C = '/eos/user/v/vshang/forTopHLT_11052023/2023C/v1ForEle/result/eff.root' 
    # in2023D = '/eos/user/v/vshang/forTopHLT_11052023/2023D/v1ForEle/result/eff.root' 
    # in2022 = '/eos/user/v/vshang/forTopHLT_11052023/2022/v1ForEle/result/eff.root' 
    # ifHadronic = False
    
    # era = uf.getEra(in2023B)
    if ifHadronic:
        plotOverLayHard(in2023D, in2024C) 
    else:
        plotEffOverLayEle(in2023B, in2023C, in2023D, in2022)


def plotEffOverLayEle(in2023B, in2023C, in2023D, in2022):
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleJet', 'ele1pt')
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleHT', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleJet', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleHT', 'ele1pt')
        
    
def plotOverLayHard(in2023D, in2024C): 
    plotEffOverlay(in2023D, in2024C, trigger='1btag', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, trigger='2btag', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, trigger='both', ifHadronic=True)
    
    plotEffOverlay(in2023D, in2024C, '1btag', 'bjetNum', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, '2btag', 'bjetNum', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, 'both', 'bjetNum', ifHadronic=True)
    
    plotEffOverlay(in2023D, in2024C, '1btag', 'HT', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, '2btag', 'HT', ifHadronic=True)
    plotEffOverlay(in2023D, in2024C, 'both', 'HT', ifHadronic=True)
    
    
    
    
def plotEffOverlay(in2023D, in2024C, trigger='1btag', var = 'jetNum', ifHadronic=False):    

    if ifHadronic:
        # eff_2023B = ph.getEffFromFile(in2023B, ['de_'+var, 'nu_'+var+'_'+trigger])
        # eff_2023C = ph.getEffFromFile(in2023C, ['de_'+var, 'nu_'+var+'_'+trigger])
        eff_2023D = ph.getEffFromFile(in2023D, ['de_'+var, 'nu_'+var+'_'+trigger])
        eff_2024C = ph.getEffFromFile(in2024C, ['de_'+var, 'nu_'+var+'_'+trigger])
        xmin, xmax = ph.getXrangeFromFile(in2024C, ['de_'+var, 'nu_'+var+'_'+trigger])
    else:
        # eff_2023B = ph.getEffFromFile(in2023B, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        # eff_2023C = ph.getEffFromFile(in2023C, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        eff_2023D = ph.getEffFromFile(in2023D, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        eff_2024 = ph.getEffFromFile(in2022, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        xmin, xmax = ph.getXrangeFromFile(in2022, ['de_'+var+'_'+trigger, 'nu_'+var+'_'+trigger])
        
    histList = [eff_2024C,eff_2023D]
    #legendList = ['2024C', '2023D']
    legendList = ['2024D_preCalib', '2024D_postCalib']
    #histList = [eff_2023B, eff_2023C]
    #legendList = ['2023B', '#splitline{2023C}{#splitline{(pre HCAL}{scale change)}}']
    outDir = getOutDir(in2024C) 
    plotName = outDir + 'HLTEff_'+var+'_'+trigger+'.png'
    ph.plotOverlay(histList, legendList, '2023', 'L1T+HLT efficiency', plotName, xmin, xmax, [0, 1.1])
   

 
#deprecated!!!
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

    
   
#deprecated!!!
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
     
    
#deprecated!!!
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
    
