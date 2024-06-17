#!/bin/bash
cd /afs/cern.ch/user/v/vshang/public/TOPHLTeff/
lines=(`cat /afs/cern.ch/user/v/vshang/public/TOPHLTeff/input/Muon2024D.txt`)
echo ${lines[$1]}
python3 skimNano.py --arg1 ${lines[$1]}  --arg2 /eos/user/v/vshang/forTopHLT_05072024/2024DpreCalib/v1ForHadronic/  --arg3 True 
