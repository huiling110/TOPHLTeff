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
    # in2024D = '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/result/eff.root'
    # in2024E = '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/result/eff.root'
    # in2024C = '/eos/home-h/hhua/forTopHLT/2024C/v2HadronicWithRdataframe/result/eff.root'
    # ifHadronic =True
    # effList = [
    #     '/eos/home-h/hhua/forTopHLT/2024C/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    #     '/eos/home-h/hhua/forTopHLT/2024D/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    #     '/eos/home-h/hhua/forTopHLT/2024E/v2HadronicWithRdataframe/result/v0ttHPhasephase/eff.root',
    # ]
    effList = [
        # '/eos/home-h/hhua/forTopHLT/2024D/v1EleTTPhase/result/v0tt/eff.root',
        # '/eos/home-h/hhua/forTopHLT/2024E/v1EleTTPhase/result/v0tt/eff.root',
        '/eos/home-h/hhua/forTopHLT/2024D/v1EleTTPhase/result/v1ttAndHT200/eff.root',
        '/eos/home-h/hhua/forTopHLT/2024E/v1EleTTPhase/result/v1ttAndHT200/eff.root',
    ]
    ifHadronic = False
    
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
    # if ifHadronic:
    #     plotOverLayHard(in2023D, in2024C) 
    # else:
    #     plotEffOverLayEle(in2023B, in2023C, in2023D, in2022)
    effVsEras(effList, ifHadronic)
    
    # eff_HHVsAll(effList[2])

def eff_HHVsAll(inputList):
    varList = ['HT', 'jet_6pt', 'nb']
    for iVar in varList:
        eff_hardAll = ph.getEffFromFile(inputList, [f'de_{iVar}_HLTAll', f'nu_{iVar}_HLTAll'])
        eff_HH = ph.getEffFromFile(inputList, [f'de_{iVar}_HH', f'nu_{iVar}_HH'])
        effList = [eff_hardAll, eff_HH]
        # legendList = ['Hardronic triggers', 'HH parking trigger'] 
        legendList = ['HT450+6jet+1btag || HT400+6jet+2btag || HT330+4jet+3btag', 'HT280+4jet+2btag']
    
        xmin = effList[0].GetTotalHistogram().GetXaxis().GetXmin()
        xmax = effList[0].GetTotalHistogram().GetXaxis().GetXmax()
        plotName = f'{getOutDir(inputList)}HLTEff_{iVar}_HHVsAll.png'
        ph.plotOverlay(effList, legendList, 'L1T+HLT efficiency', plotName, xmin, xmax, ['2024E'], [0, 1.1], [0.2, 0.25, 0.9, 0.5])
        

# def effVsEras(inputList, HLT='HLTAll', ifHadronic=True):
def effVsEras(inputList, ifHadronic=True):
    outDir = getOutDir(inputList[0])
   
    if ifHadronic:
        varList = ['HT', 'jet_6pt', 'nb']
        HLT = 'HLTALL'
    else:
        varList = ['ele_1pt', 'ele_1eta', 'HT']
        # HLT = 'HLTcrossEle'
        HLT = 'HLTbothEle'
        
    for iVar in varList:
        effList = []
        eraList = []
        for iEff in inputList:
            # eff = ph.getEffFromFile(iEff, [f'de_{iVar}_HLTAll', f'nu_{iVar}_HLTAll'])
            eff = ph.getEffFromFile(iEff, [f'de_{iVar}_{HLT}', f'nu_{iVar}_{HLT}'])
            era = uf.getEra(iEff)
            effList.append(eff)
            eraList.append(era)
        print(effList) 
        
        xmin = effList[0].GetTotalHistogram().GetXaxis().GetXmin()
        xmax = effList[0].GetTotalHistogram().GetXaxis().GetXmax()
        
        # plotName =  f'{outDir}HLTEff_{iVar}_HLTAll.png'
        plotName =  f'{outDir}HLTEff_{iVar}_{HLT}.png'
        ph.plotOverlay(effList, eraList,  'L1T+HLT efficiency', plotName, xmin, xmax, eraList, [0, 1.1])
    
    
    

def plotEffOverLayEle(in2023B, in2023C, in2023D, in2022):
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleJet', 'ele1pt')
    plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'eleHT', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleJet', 'ele1pt')
    # plotEffOverlay(in2023B, in2023C, in2023D, in2022, 'singleEleHT', 'ele1pt')
        
    
def plotOverLayHard(in2023D, in2024C): 
    # plotEffOverlay(in2023D, in2024C, trigger='1btag', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, trigger='2btag', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, trigger='both', ifHadronic=True)
    
    # plotEffOverlay(in2023D, in2024C, '1btag', 'bjetNum', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, '2btag', 'bjetNum', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, 'both', 'bjetNum', ifHadronic=True)
    
    # plotEffOverlay(in2023D, in2024C, '1btag', 'HT', ifHadronic=True)
    # plotEffOverlay(in2023D, in2024C, '2btag', 'HT', ifHadronic=True)
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
   

 
    

 
   
    
def getOutDir(inputFile):
    inputDir = inputFile.rsplit('/', 1)[0] +'/'
    outDir = inputDir+'results/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    return outDir
     
    
        
    
if __name__=='__main__':
    main() 
    
