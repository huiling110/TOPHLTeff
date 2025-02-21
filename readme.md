# Set up enviroment
- ``` bash setEnv.sh ```
- ```voms-proxy-init --voms cms```



# Get input nanoAOD list
- ```python3 generateInputList.py```

# Skim nanoAOD
- Test locally 
   ```python3 skimNano.py```
- Submit jobs
    ```python3 subJobs.py```
    - check job

# Plot HLT efficiency
- Generate HLT efficieny hists
```python3 plotHLT.py```

- Plot efficieny 
```python3 plotEff.py```


# To do
- [] Make the workflow more automated 
- [] Setup enviroment properly in CenOS9
- [] Intergate nanoAOD tool data format for object selection
- [] Check the btag change during data taking