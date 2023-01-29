import plotly.express as p
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.figure_factory as pt


def helper(df):
    df1 = df.drop_duplicates(subset=['Team', 'NOC', 'Games',
                                     'Year', 'City', 'Sport', 'Event', 'Medal', 'region',
                                     'Bronze', 'Gold', 'Silver'])

    df1["Bronze"] =  df1["Bronze"].astype(int)
    df1["Gold"] = df1["Gold"].astype(int)
    df1["Silver"] = df1["Silver"].astype(int)



    medal_info = df1.groupby("NOC").sum()[["Gold", "Silver","Bronze"]].sort_values("Gold",
                                                                                    ascending=False).reset_index()
    medal_info["Total"] = medal_info["Bronze"] + medal_info["Gold"] + medal_info["Silver"]


    return medal_info,df1

def getyear_region(df):
    h = df["Year"].unique().tolist()
    h.sort()
    h.insert(0, "overall")
    g = df["region"].dropna().unique().tolist()
    t = sorted(g)
    t.insert(0, "overall")
    return h,t


def fetch_medal(df1,year, country):
    if year == "overall" and country == "overall":
        df = df1
    if year != "overall" and country == "overall":
        df = df1[df1["Year"] == year]
    if year == "overall" and country != "overall":
        df = df1[df1["region"] == country]
    if year != "overall" and country != "overall":
        df = df1[(df1["Year"] == year) & (df1["region"] == country)]

    x = df.groupby("NOC").sum()[[ "Gold", "Silver","Bronze"]].sort_values("Gold", ascending=False).reset_index()
    x["Total"] = x["Bronze"] + x["Gold"] + x["Silver"]

    return x

def plot(df1,col):
    noofcoun_peryear = df1.drop_duplicates(subset=["Year", col])["Year"].value_counts().reset_index().sort_values(
        "index")
    noofcoun_peryear.rename(columns={"index": "Year", "Year": col}, inplace=True)

    return noofcoun_peryear

def ploted(df1):
    noofcoun_peryear = df1.drop_duplicates(subset=["Year", "Sport", "Event"])
    return noofcoun_peryear


def get_rank(df2,sport=None):
    df1 = df2.drop_duplicates(subset=["Medal","Sport","region","Name","Year","Event"]).dropna(subset=["Medal","region"])
    df3 = df1.groupby("Name").count()["Medal"].reset_index().sort_values("Medal",ascending=False)
    df4 = df3.merge(df2,on="Name")[["Name","Medal_x","NOC","Sport"]].drop_duplicates(subset=["Name","Medal_x","Sport","NOC"])
    df5 = df4.rename(columns={"Medal_x":"Medals","NOC":"Country"})
    if(sport == None or sport == "overall"):
        df5 = df5.head(15)
    else:
        df5 = df5[df5["Country"] == sport]
    return df5


def get_contry(df,country):
    new_df = df[df["NOC"] == country ].dropna(subset=["Medal"]).drop_duplicates(subset=["NOC","Sport","Event","Medal","Year"])[["Year","Medal"]]
    new = new_df.groupby("Year").count().reset_index()
    fig = p.line(new,x="Year",y="Medal")

    return fig


def get(df,country):
    new = df[df["NOC"] == country]
    dfe = new.dropna(subset=["Medal"]).drop_duplicates(subset=["Name", "Sport", "Year", "NOC", "Event", "Medal"])
    new1 = pd.pivot_table(dfe, index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0)
    j = new1.astype(int)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(j, annot=True)
    return st.pyplot(fig)


def get_contry2(df,country,top):
    new_df = df[df["NOC"] == country ].dropna(subset=["Medal"]).drop_duplicates(subset=["NOC","Sport","Event","Medal","Year"])[["Name","Medal"]]
    new = new_df.groupby("Name").count().reset_index().sort_values("Medal",ascending=False).merge(df,on="Name")[["Name","Medal_x","NOC"]].drop_duplicates().rename(columns={"Medal_x":"Medal"}).head(top)
    return st.table(new)

def get_graph(df):
    df["Age"].isnull().sum()
    df1 = df.dropna(subset=["Age"])
    x0 = df1["Age"]
    x1 = df1[df1["Medal"] == "Gold"]["Age"]
    x2 = df1[df1["Medal"] == "Silver"]["Age"]
    x3 = df1[df1["Medal"] == "Bronze"]["Age"]
    fig = pt.create_distplot([x0, x1, x2, x3], ["Overall_age","Gold","Silver","Bronze"], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=950,height=600)
    return fig


def get_sport_age(df):
    X = []
    name = []
    dfk = df.dropna(subset=["Age"])
    for x in list(dfk.Sport.unique()):
        x1 = dfk[dfk["Sport"] == x]
        get = x1[x1["Medal"] == "Gold"]["Age"]
        X.append(get)
        name.append(x)

    return pt.create_distplot([X[0],X[1],X[2],X[3],X[4],X[5]],[name[0],name[1],name[2],name[3],name[4],name[5]],show_hist=False,show_rug=False)

def get1(df,sport):
    dfv = df.dropna(subset=["Height", "Weight"]).fillna("No_Medal")
    get = dfv[dfv["Sport"] == sport][["Height","Weight","Medal","Sex"]]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax = sns.scatterplot(x=get.Height,y=get.Weight,hue=get.Medal,style=get.Sex,s=200)
    return fig


def plot_sex(df):
    df = df.drop_duplicates(subset=['Team', 'NOC', 'Games',"Sex",
                            'Year', 'City', 'Sport', 'Event', 'Medal', 'region'])
    df1 = df[df["Sex"]=="M"].groupby("Year").count()["Sex"].reset_index()
    df2 = df[df["Sex"]=="F"].groupby("Year").count()["Sex"].reset_index()
    df4 = df1.merge(df2,on="Year")
    df4 = df4.rename(columns={"Sex_x":"Male","Sex_y":"Female"})
    return st.plotly_chart(p.line(df4,x="Year",y=["Male","Female"]))