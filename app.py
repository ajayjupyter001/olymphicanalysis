import streamlit as st
import pandas as pd
import plotly.express as p
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns

data = preprocess.preprocess()
st.sidebar.image("olum.png")
st.sidebar.title("Olympic Analysis")
option = st.sidebar.radio(
    "Select the option",
    ("Medal Info","Overall Analysis","Countary-wise Analysis","Athletic-wise Analysis")
)


if option == "Medal Info":
    st.sidebar.header("Medal Info")
    year,region= helper.getyear_region(data)
    selected_year = st.sidebar.selectbox("Year",year)
    selected_region = st.sidebar.selectbox("Country", region)
    if(selected_year=="overall" and selected_region == "overall"):
        st.title("Overall Info")

    elif(selected_year != "overall" and selected_region == "overall"):
        st.title("Medal Info of overall country in {}".format(selected_year))

    elif(selected_year == "overall" and selected_region == "overall"):
        st.title("Medal Info of {} in overall year".format(selected_region))

    else:
        st.title("Medal Info of {} in {}".format(selected_region,selected_year))

    d,k = helper.helper(data)
    j = helper.fetch_medal(k,selected_year,selected_region)
    st.table(j)


if option == "Overall Analysis":
    d, df1 = helper.helper(data)
    total = len(sorted(df1["Year"].unique().tolist())) - 1
    total_play = df1["Name"].unique().shape[0]
    total_city = df1["City"].unique().shape[0]
    total_country = df1["region"].unique().shape[0]
    total_events = df1["Event"].unique().shape[0]
    total_sports = df1["Sport"].unique().shape[0]

    st.header("Overall Statictics")
    col1,col2,col3= st.columns(3)


    with col1:
        st.header("Years")
        st.title(total)
    with col2:
        st.header("Athletics")
        st.title(total_play)
    with col3:
        st.header("Host")
        st.title(total_city)

    col4, col5,col6= st.columns(3)

    with col4:
        st.header("Countries")
        st.title(total_country)
    with col5:
        st.header("Events")
        st.title(total_events)
    with col6:
        st.header("Sports")
        st.title(total_sports)

    st.header("Year vs No of Region(Countries)")
    fig = helper.plot(df1,"region")
    fig1 = p.line(fig,x="Year",y="region")
    st.plotly_chart(fig1)

    st.header("Year vs No of Event")
    fig = helper.plot(df1, "Event")
    fig1 = p.line(fig, x="Year", y="Event")
    st.plotly_chart(fig1)

    st.header("Year vs No of Athletics")
    fig = helper.plot(df1, "Name")
    fig1 = p.line(fig, x="Year", y="Name")
    st.plotly_chart(fig1)

    st.title("No of Events Over Time")
    noofcoun_peryear = helper.ploted(df1)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pd.pivot_table(noofcoun_peryear, index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"), annot=True)
    st.pyplot(fig)

    st.title("Successfull Athlets")
    new = pd.Series(df1.NOC.unique()).sort_values(0).to_list()
    new.insert(0, "overall")
    select = st.selectbox("Select top rank player over country",
                         new)
    st.table(helper.get_rank(df1,select))

if option == "Countary-wise Analysis":
    st.title("Year vs Medals over countries")
    st.sidebar.title("Countary-wise Analysis")
    new = pd.Series(data.NOC.unique()).sort_values(0).to_list()
    select = st.sidebar.selectbox("Select the country",new)
    st.plotly_chart(helper.get_contry(data,select))
    st.title("No of Medals over Events")
    try:
        helper.get(data,select)
    except:
        st.header("No data")
    st.title("Top players in {}".format(select))
    y = st.selectbox("Select N top players",[i for i in range(5,20,1)])
    helper.get_contry2(data,select,y)

if option == "Athletic-wise Analysis":
    st.title("Medals over Age")
    st.plotly_chart(helper.get_graph(data))
    st.title("Medal got in Sports over Age")
    st.plotly_chart(helper.get_sport_age(data))
    st.title("Height vs Weight over Sport")
    select = st.selectbox("Choose the Sport",data.Sport.unique())
    st.pyplot(helper.get1(data,select))
    st.title("Sex over years")
    helper.plot_sex(data)