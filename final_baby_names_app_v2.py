
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("https://data.cityofnewyork.us/api/views/25th-nujf/rows.csv?accessType=DOWNLOAD")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("'", "")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🎛️ Filter Options")
year = st.sidebar.selectbox("Select Year", sorted(df["year_of_birth"].unique(), reverse=True))
gender = st.sidebar.selectbox("Select Gender", sorted(df["gender"].unique()))
ethnicity = st.sidebar.selectbox("Select Ethnicity", sorted(df["ethnicity"].unique()))
name_input = st.sidebar.text_input("Search for a Name", "Olivia")  # Default value for demo

st.title("🍼 NYC Popular Baby Names Dashboard")

# Filtered Data
filtered_df = df[(df["year_of_birth"] == year) & 
                 (df["gender"] == gender) & 
                 (df["ethnicity"] == ethnicity)]

# Top Names Bar Chart
st.subheader(f"Top 10 Names in {year} ({gender}, {ethnicity})")
top_names = filtered_df.sort_values(by="count", ascending=False).head(10)
fig1 = px.bar(top_names, x="childs_first_name", y="count",
              labels={"childs_first_name": "Name", "count": "Number of Babies"},
              title="Top 10 Baby Names")
st.plotly_chart(fig1)

# Name Trend Over Time
if name_input:
    st.subheader(f"Trend of '{name_input.title()}' Over Time")
    name_df = df[df["childs_first_name"].str.lower() == name_input.lower()]
    if not name_df.empty:
        fig2 = px.line(name_df, x="year_of_birth", y="count", color="gender",
                       title=f"Name Trend: {name_input.title()}",
                       labels={"year_of_birth": "Year", "count": "Count"})
        st.plotly_chart(fig2)
    else:
        st.warning(f"No data found for the name '{name_input}'.")

# Ethnicity Distribution for the Name
if name_input:
    st.subheader(f"Ethnic Distribution of '{name_input.title()}' in {year}")
    pie_df = df[(df["childs_first_name"].str.lower() == name_input.lower()) &
                (df["year_of_birth"] == year)]
    if not pie_df.empty:
        fig3 = px.pie(pie_df, names="ethnicity", values="count",
                      title="Ethnic Breakdown")
        st.plotly_chart(fig3)

# Summary Table
if name_input:
    st.subheader(f"Summary Table for '{name_input.title()}'")
    summary = df[df["childs_first_name"].str.lower() == name_input.lower()]
    if not summary.empty:
        summary_table = summary.groupby(["year_of_birth", "gender", "ethnicity"])["count"].sum().reset_index()
        st.dataframe(summary_table)
    else:
        st.info("No summary data available.")
else:
    st.info("⬅️ Try searching for a name in the sidebar to unlock more insights!")
