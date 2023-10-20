#!/bin/bash
cd /afs/cern.ch/user/v/vshang/public/TOPHLTeff/
lines=(`cat /afs/cern.ch/user/v/vshang/public/TOPHLTeff/input/Muon2023D.txt`)
echo ${lines[$1]}
python3 skimNano.py --arg1 ${lines[$1]}  --arg2 /eos/user/v/vshang/forTopHLT/2023D/v1forEle/  --arg3 True 
