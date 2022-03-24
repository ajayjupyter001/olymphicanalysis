import pandas as pd

df = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")

def preprocess():
    df1 = df.merge(noc, on="NOC")
    df2 = df1[df1["Season"] == "Summer"]
    df3 = df2.drop_duplicates()
    new = pd.get_dummies(df3["Medal"])
    df4 = pd.concat([df3, new], axis=1)

    return df4