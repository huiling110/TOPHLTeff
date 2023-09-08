# Set up enviroment
- ``` bash setEnv.sh ```
- ```voms```



# Get input nanoAOD list
- ```python3 generateInputList.py```

# Skim nanoAOD
- Test locally 
   ```python3 skimNano.py```
- Submit jobs
    ```python3 subJobs.py```

# Plot HLT efficiency
- Generate HLT efficieny hists
```python3 plotHLT.py```

- Plot efficieny 
```python3 plotEff.py```


# To do
[ ]  Switch to TEfficiency for efficiency calculation
- [] Intergate nanoAOD tool data format for object selection
- [] Check the btag change during data taking