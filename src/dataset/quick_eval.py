import pandas as pd
import numpy as np

def eval2(dataset: pd.DataFrame, dimensions):
    complete = list(range(1, 25))
    total = 0
    for val in dataset["Age in 5-year groups"].unique():
        rows = dataset[(dataset["Age in 5-year groups"] == val) & (dataset["Type of place of residence"] == "rural")]
        res = rows["Number of household members"].unique().tolist()
        total = total + len(np.setdiff1d(complete, res))
    print(total)

def eval3(dataset: pd.DataFrame, dimensions):
    complete = list(range(1, 25))
    total = 0
    for val in dataset["Age in 5-year groups"].unique():
        for val2 in dataset["Number of household members"].unique():
            rows = dataset[(dataset["Age in 5-year groups"] == val) & (dataset["Type of place of residence"] == "rural") & (dataset["Number of household members"] == val2)]
            print(val + " + " + "rural + " + str(val2) +  " = " + str(len(rows["Number of household members"])))