

import ROOT
from globeVariables import lumiMap


def setMyStyle():
    myStyle = ROOT.TStyle("tdrStyle","Style for P-TDR")

    myStyle.SetCanvasBorderMode(0)
    myStyle.SetCanvasColor(ROOT.kWhite)
    myStyle.SetCanvasDefH(600)
    myStyle.SetCanvasDefW(600)
    myStyle.SetCanvasDefX(0)
    myStyle.SetCanvasDefY(0)

    myStyle.SetPadBorderMode(0)
    myStyle.SetPadColor(ROOT.kWhite)
    myStyle.SetPadGridX(ROOT.kFALSE)
    myStyle.SetPadGridY(ROOT.kTRUE) 

    myStyle.SetFrameBorderMode(0)
    myStyle.SetFrameBorderSize(1)
    myStyle.SetFrameFillColor(0)
    myStyle.SetFrameFillStyle(0)
    myStyle.SetFrameLineColor(1)
    myStyle.SetFrameLineStyle(1)
    myStyle.SetFrameLineWidth(1)

    myStyle.SetPadTopMargin(0.07)
    myStyle.SetPadBottomMargin(0.13)
    myStyle.SetPadLeftMargin(0.16)
    myStyle.SetPadRightMargin(0.1)
    
        #hist settings
    myStyle.SetHistLineColor(ROOT.kBlack)
    #   myStyle.SetHistLineStyle(0)
    myStyle.SetHistLineWidth(2)
    myStyle.SetEndErrorSize(2)
    #   myStyle.SetErrorX(0.) #error bar no x 
    myStyle.SetMarkerStyle(20)
    myStyle.SetMarkerSize(2)

    #   myStyle.SetOptFit(1)
    #   myStyle.SetFitFormat("5.4g")
    #   myStyle.SetFuncColor(2)
    #   myStyle.SetFuncStyle(1)
    #   myStyle.SetFuncWidth(1)

    #   myStyle.SetOptDate(0)

    #   myStyle.SetOptFile(0)
    myStyle.SetOptStat(0) 
    myStyle.SetStatColor(ROOT.kWhite)
    myStyle.SetStatFont(42)
    myStyle.SetStatFontSize(0.025)
    myStyle.SetStatTextColor(1)
    myStyle.SetStatFormat("6.4g")
    myStyle.SetStatBorderSize(1)
    myStyle.SetStatH(0.1)
    myStyle.SetStatW(0.15)


    myStyle.SetOptTitle(0)
    myStyle.SetTitleFont(42)
    myStyle.SetTitleColor(1)
    myStyle.SetTitleTextColor(1)
    myStyle.SetTitleFillColor(10)
    myStyle.SetTitleFontSize(0.05)

    #  # //Axis titles:
    #   myStyle.SetTitleColor(1,"XYZ")
    #   myStyle.SetTitleFont(42,"XYZ")
    myStyle.SetTitleSize(0.06,"XYZ")
    #   myStyle.SetTitleXOffset(0.9)
    #   myStyle.SetTitleYOffset(1.25)
    

    myStyle.SetLabelColor(1, "XYZ")
    myStyle.SetLabelFont(42,"XYZ")
    myStyle.SetLabelOffset(0.007, "XYZ")
    myStyle.SetLabelSize(0.04, "XYZ")

    #   myStyle.SetAxisColor(1, "XYZ")
    #   myStyle.SetStripDecimals(ROOT.kTRUE)
    #   myStyle.SetTickLength(0.03, "XYZ")
    #   myStyle.SetNdivisions(510, "XYZ")
    #   myStyle.SetPadTickX(1)  
    #   myStyle.SetPadTickY(1)


    #   myStyle.SetOptLogx(0)
    #   myStyle.SetOptLogy(0)
    #   myStyle.SetOptLogz(0)

    #   myStyle.SetPaperSize(20.,20.)
    
    #   myStyle.cd()
    return myStyle




def addCMSTextToCan(canvas, x1=0.23, x2=0.35,x3=0.7, y=0.96, era = '2016', isRun3=False):
    can = canvas
     
    cmsTextFont = 61
    extraTextFont = 52
    cmsText = "CMS"
    extraText = "Preliminary "# + era
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(31)
    #latex.SetTextSize(0.04)
    latex.SetTextSize(0.05)
    latex.SetTextFont(cmsTextFont)
    latex.DrawLatex(x1, y, cmsText )
    latex.SetTextFont(extraTextFont)
    #latex.SetTextSize(0.04*0.76)
    latex.SetTextSize(0.05*0.76)
    latex.DrawLatex(x2, y , extraText )
  
    lumiText = lumiMap[era] /1000
    lumiText_s = '35.2 fb^{-1}, 2022 + 27.2 fb^{-1}, 2023'
    #lumiText_s = '2022-2023D'
    energy = '13'
    if isRun3:
        energy = '13.6'
    #lumiText_s = lumiText_s + ' fb^{-1}('+ energy +'TeV)'
    lumiText_s = lumiText_s + ' ('+ energy +' TeV)'
    # print(lumiText)
    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.038)
    latex2.SetTextAlign(31)
    latex2.SetTextFont(42)  
    # latex2.DrawLatex(x2+0.6, y, lumiText_s )
    latex2.DrawLatex( x3, y, lumiText_s )


def addTriggerInfo(ifHadronic=True):
    if ifHadronic:
        #triggerText = '#splitline{Online requirements:}{#splitline{Six jets with p_{T} > 36 GeV,}{#splitline{1 b-tagged jet,}{and H_T > 450 GeV}}}'
        #triggerText = '#splitline{Online requirements:}{#splitline{Six jets with p_{T} > 32 GeV,}{#splitline{2 b-tagged jets,}{and H_T > 400 GeV}}}'
        triggerText = '#splitline{Online requirements:}{#splitline{Six jets with p_{T} > 32 GeV,}{#splitline{1 or 2 b-tagged jets,}{and H_T > 400 GeV}}}'
    else:
        #triggerText = '#splitline{Online requirements:}{#splitline{Electron with p_{T} > 28 GeV}{and H_T > 150 GeV}}'
        #triggerText = '#splitline{Online requirements:}{#splitline{Electron with p_{T} > 30 GeV}{and jet with p_{T} > 35 GeV}}'
        #triggerText = '#splitline{Online requirements:}{#splitline{Electron with p_{T} > 28 GeV}{#splitline{and H_T > 150 GeV}{#splitline{(excluding BPix region with}{-1.8 < #eta < 0.6 and -1.5 < #phi < -0.5)}}}}'
        triggerText = '#splitline{Online requirements:}{#splitline{Electron with p_{T} > 30 GeV}{#splitline{and jet with p_{T} > 35 GeV}{#splitline{(excluding BPix region with}{-1.8 < #eta < 0.6 and -1.5 < #phi < -0.5)}}}}'

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(31)
    latex.SetTextFont(42)
    latex.DrawLatex(0.65, 0.4, triggerText)
