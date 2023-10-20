#!/bin/bash
cd /afs/cern.ch/user/v/vshang/public/TOPHLTeff/
lines=(`cat /afs/cern.ch/user/v/vshang/public/TOPHLTeff/input/Muon2023C.txt`)
echo ${lines[$1]}
python3 skimNano.py --arg1 ${lines[$1]}  --arg2 /eos/user/v/vshang/forTopHLT/2023C/v1ForHardronicv2/  --arg3 True 
