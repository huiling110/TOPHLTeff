
import ROOT
import setTDRStyle as st


def getEffFromFile(inputDirFile, Histlist):   
    b_eta1List= getHistFromFile( inputDirFile, Histlist) 
    #    print(b_eta1List)
    eff_b_eta1 = ROOT.TEfficiency( b_eta1List[1], b_eta1List[0] ) #num = b_eta1List[1], denom = b_eta1List[0]
    eff_b_eta1.Print()
    return eff_b_eta1

def getXrangeFromFile(inputDirFile, Histlist):
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
     
    


def plotOverlay(histList, legenList, era, yTitle, plotName, xmin, xmax, yRange=[]):
    print('start to plot overlay plot')
    mySty =  st.setMyStyle()
    mySty.cd()
    ROOT.gROOT.SetBatch(True)
    can = ROOT.TCanvas('overlay', 'overlay', 1000, 800)
    
    # legend = ROOT.TLegend(0.65, 0.8, 0.9, 0.93)  # Create a legend to label the histograms
    legend = ROOT.TLegend(0.7, 0.2, 0.9, 0.53)  # Create a legend to label the histograms
    
    #yMax = getYmax(histList)
    #plot style
    LineColorDic={
        # 0: ROOT.TColor.GetColor("#fdae61"),
        # 0: ROOT.TColor.GetColor("#fd8d3c"),
        # 1: ROOT.TColor.GetColor("#f03b20"),
        # 2: ROOT.TColor.GetColor("#2ca25f"),
        # 3: ROOT.TColor.GetColor("#d01c8b"),
        0: ROOT.TColor.GetColor("#fdae61"),
        1: ROOT.TColor.GetColor("#d01c8b"),
        #2ca25f green
        #d01c8b purple
        ##fdae61 fc9272" orange
    }
    

    for i, histogram in enumerate(histList):
        if i == 0:
            histogram.Draw()  # Draw the first histogram without any options
        else:
            histogram.Draw("same")  # Draw subsequent histograms with "same" option to overlay

        histogram.SetLineColor(LineColorDic[i])
        histogram.SetMarkerColor(LineColorDic[i])
        histogram.SetLineWidth(3)  # Set line width for each histogram
        histogram.SetMarkerSize(1.5)
        # histogram.SetMarkerStyle(45)
        histogram.SetMarkerStyle(64)
        # histogram.GetXaxis().SetTitle(histogram.GetTitle())  # Set X-axis title (modify as needed)
        # histogram.GetYaxis().SetTitle(yTitle)  # Set Y-axis title (modify as needed)
        # histogram.GetXaxis().SetTitleSize(0.05)
        # histogram.GetYaxis().SetTitleSize(0.05)
        xTitle = histogram.GetCopyTotalHisto().GetTitle()
        histogram.SetTitle(";"+xTitle+";"+yTitle)
        ROOT.gPad.Update()
        histogram.GetPaintedGraph().GetXaxis().SetTitleSize(0.05)
        histogram.GetPaintedGraph().GetYaxis().SetTitleSize(0.05)
        # if len(yRange)>1:
        #     histList[i].GetYaxis().SetRangeUser(yRange[0], yRange[1])
        # else:
        #     histList[i].GetYaxis().SetRangeUser(0, yMax*1.3)
        histogram.GetPaintedGraph().SetMinimum(yRange[0])
        histogram.GetPaintedGraph().SetMaximum(yRange[1])
        histogram.GetPaintedGraph().GetXaxis().SetLimits(xmin, xmax)
        
        legend.AddEntry(histogram, legenList[i], "l")  # Add an entry to the legend
        legend.Draw() 
        
    #st.addCMSTextToCan(can, 0.22, 0.34, 0.9, 0.94, era, True)
    # st.addCMSTextToCan(can, 0.24, 0.39, 0.9, 0.94, era, True)
    st.addTriggerInfo(ifHadronic=True)
    #st.addTriggerInfo(ifHadronic=False)
    
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
