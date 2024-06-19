
import ROOT
import setTDRStyle as st


def getEffFromFile(inputDirFile, Histlist):   
    b_eta1List= getHistFromFile( inputDirFile, Histlist) 
    #    print(b_eta1List)
    eff_b_eta1 = ROOT.TEfficiency( b_eta1List[1], b_eta1List[0] ) #num = b_eta1List[1], denom = b_eta1List[0]
    eff_b_eta1.Print()
    return eff_b_eta1

def getXrangeFromFile(inputDirFile, Histlist):
#!redundent function 
    b_eta1List= getHistFromFile( inputDirFile, Histlist)
    xmin = b_eta1List[0].GetXaxis().GetXmin()
    xmax = b_eta1List[0].GetXaxis().GetXmax()
    print("xmin = ", int(xmin), ", xmax = ", int(xmax))
    return int(xmin), int(xmax)
 

#Deprecated
def getEff(de, nu) :
    #!!! use maybe TEfficiency later to calculate efficiency
    de_d = de.Clone()
    nu_d = nu.Clone()
    # de.Print()
    de_d.Sumw2()
    nu_d.Sumw2()
    eff = de_d.Clone()
    # eff.Print()
    eff.Reset()
    # eff.Print()
    eff.Divide(nu_d, de_d)
    # eff.Print()
    return eff


def getHistFromFile(fileName, histNames):
    file = ROOT.TFile.Open(fileName)

    if not file or file.IsZombie():
        print("Error: Unable to open the file.")
        return []

    histograms = []
    # Loop through the list of histogram names
    for name in histNames:
        # Get the histogram from the file
        histogram = file.Get(name)
        histogram.Print()
        if not histogram:
            print("Error: Unable to find the histogram", name, "in the file.")
            continue
        # Clone the histogram to avoid potential issues when the file is closed
        histogram1 = histogram.Clone()
        # histogram1.Print()
        histogram1.SetDirectory(0)
        histograms.append(histogram1)
    # Close the file (optional, depending on your use case)
    file.Close()

    return histograms
     
    


def plotOverlay(histList, legenList,   yTitle, plotName, xmin, xmax,  era=['2024'] , yRange=[0, 1], legendPos=[0.7, 0.2, 0.9, 0.53], ifExtraTxt=False):
    print('start to plot overlay plot')
    mySty =  st.setMyStyle()
    mySty.cd()
    ROOT.gROOT.SetBatch(True)
    can = ROOT.TCanvas('overlay', 'overlay', 1000, 800)
    
    legend = st.getMyLegend(legendPos[0], legendPos[1], legendPos[2], legendPos[3])
    LineColorDic={
        0: [ROOT.TColor.GetColor("#f03b20"), 8], #rea
        1: [ROOT.TColor.GetColor("#fd8d3c"), 41], #orange
        # 2: [ROOT.TColor.GetColor("#2ca25f"), 101],
        2: [ROOT.TColor.GetColor("#2ca25f"), 1], #green
        #2ca25f green
        #d01c8b purple
        ##fdae61 fc9272" orange
    }
    

    for i, histogram in enumerate(histList):
        if i == 0:
            histogram.Draw()  # Draw the first histogram without any options
        else:
            histogram.Draw("same")  # Draw subsequent histograms with "same" option to overlay

        # histogram.SetLineColor(LineColorDic[i])
        # histogram.SetMarkerColor(LineColorDic[i])
        histogram.SetLineWidth(3)  # Set line width for each histogram
        histogram.SetMarkerSize(1.5)
        histogram.SetLineColor(LineColorDic[i][0])
        histogram.SetMarkerColor(LineColorDic[i][0])
        histogram.SetMarkerStyle(LineColorDic[i][1])
        
        xTitle = histogram.GetCopyTotalHisto().GetTitle()
        histogram.SetTitle(";"+xTitle+";"+yTitle)
        ROOT.gPad.Update()
        histogram.GetPaintedGraph().GetXaxis().SetTitleSize(0.05)
        histogram.GetPaintedGraph().GetYaxis().SetTitleSize(0.05)
        histogram.GetPaintedGraph().SetMinimum(yRange[0])
        histogram.GetPaintedGraph().SetMaximum(yRange[1])
        histogram.GetPaintedGraph().GetXaxis().SetLimits(xmin, xmax)
        
        legend.AddEntry(histogram, legenList[i], "lp")  # Add an entry to the legend
        legend.Draw() 
        
    #st.addCMSTextToCan(can, 0.22, 0.34, 0.9, 0.94, era, True)
    st.addCMSTextToCan(can, 0.24, 0.39, 0.9, 0.94, era, True)
    
    if ifExtraTxt:
        st.addTriggerInfo(ifHadronic=True)
    
    can.SaveAs(plotName)
    print('Done overlay plotting\n\n')
    
    
def getYmax(histograms):
    max_y = -1.0
    for hist in histograms:
        if hist:
            current_max_y = hist.GetMaximum()
            if current_max_y > max_y:
                max_y = current_max_y

    return max_y    
