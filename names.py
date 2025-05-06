
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('https://data.cityofnewyork.us/api/views/25th-nujf/rows.csv?accessType=DOWNLOAD')
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("'", "")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filter Options")
year = st.sidebar.selectbox("Select Year", sorted(df['year_of_birth'].unique(), reverse=True))
gender = st.sidebar.selectbox("Select Gender", df['gender'].unique())
ethnicity = st.sidebar.selectbox("Select Ethnicity", df['ethnicity'].unique())
name_input = st.sidebar.text_input("Search for a Name", "")

st.title("🍼 NYC Popular Baby Names Dashboard")

# Filtered dataframe
filtered_df = df[(df['year_of_birth'] == year) & 
                 (df['gender'] == gender) & 
                 (df['ethnicity'] == ethnicity)]

# Top Names Chart
st.subheader(f"Top Baby Names in {year} - {gender}, {ethnicity}")
top_names = filtered_df.sort_values(by='count', ascending=False).head(10)
fig1 = px.bar(top_names, x='childs_first_name', y='count', 
              labels={'childs_first_name': 'Name', 'count': 'Count'}, title="Top 10 Names")
st.plotly_chart(fig1)

# Name Trend Over Time
if name_input:
    st.subheader(f"Popularity of '{name_input}' Over Time")
    name_df = df[df['childs_first_name'].str.lower() == name_input.lower()]
    if not name_df.empty:
        fig2 = px.line(name_df, x='year_of_birth', y='count', color='gender',
                       title=f"Trend of '{name_input}' by Year and Gender",
                       labels={'year_of_birth': 'Year', 'count': 'Count'})
        st.plotly_chart(fig2)
    else:
        st.warning(f"No data found for the name '{name_input}'.")

# Ethnicity Distribution Pie Chart
if name_input:
    st.subheader(f"Ethnicity Distribution for '{name_input}' in {year}")
    pie_df = df[(df['childs_first_name'].str.lower() == name_input.lower()) & 
                (df['year_of_birth'] == year)]
    if not pie_df.empty:
        fig3 = px.pie(pie_df, names='ethnicity', values='count', title='Ethnic Breakdown')
        st.plotly_chart(fig3)

# Summary Table
if name_input:
    st.subheader(f"Summary Statistics for '{name_input}'")
    summary = df[df['childs_first_name'].str.lower() == name_input.lower()]
    if not summary.empty:
        st.dataframe(summary.groupby(['year_of_birth', 'gender', 'ethnicity'])['count'].sum().reset_index())
    else:
        st.info("No matching records found.")
