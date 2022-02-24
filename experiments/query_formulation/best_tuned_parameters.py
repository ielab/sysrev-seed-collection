import json
import os
import pandas as pd
#%%
basedir = "tuned_params_ecir/recall"
params = []
for fname in os.listdir(basedir):
    with open(f"{basedir}/{fname}", "r") as f:
        params.append(json.load(f))
pd.DataFrame(params).median()
