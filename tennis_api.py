import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

host = "localhost"
port = "5432"
database = "MDTM37DB"
username = "postgres"
password = "password"

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")


def load_data(table_1, table_2):
    merge_on = ''
    if table_1 == 'competitors':
        merge_on = "competitor_id"
    elif table_1 == 'categories':
        merge_on = 'category_id'
    elif table_1 == 'complexes':
        merge_on = 'complex_id'

    query_1 = f"SELECT * FROM {table_1}"
    query_2 = f"SELECT * FROM {table_2}"

    df_1 = pd.read_sql(query_1, engine)
    df_2 = pd.read_sql(query_2, engine)

    df = pd.merge(df_1, df_2, on=merge_on)

    return df


# Load data
competitors_rankings_df = load_data('competitors', 'competitor_rankings')
category_competitions_df = load_data('categories', 'competitions')
complex_venues_df = load_data('complexes', 'venues')

# Merge the two tables for better visualization
# df = pd.merge(rankings_df, competitors_df, on="competitor_id")

# Define Tabs
selected_tab = st.selectbox("Navigate to:",
                            ["🏠 Homepage", "🔍 Search & Filter", "📊 Competitor Details", "🌍 Country-Wise Analysis",
                             "🏆 Leaderboards"])

# 🏠 **Homepage (No Sidebar)**
if selected_tab == "🏠 Homepage":
    st.title("🎾 Tennis Analysis Dashboard")

    st.subheader('Competitors & Competitor-Rankings')
    st.dataframe(competitors_rankings_df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", competitors_rankings_df["competitor_id"].nunique())
    col2.metric("Countries Represented", competitors_rankings_df["country"].nunique())
    col3.metric("Highest Points Scored", competitors_rankings_df["points"].max())

    st.subheader('Categories & Competitions')
    st.dataframe(category_competitions_df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Category", category_competitions_df["category_name"].nunique())
    col2.metric("No.of Category Type", category_competitions_df["type"].nunique())
    col3.metric("Gender", 'Men Women')

    st.subheader('Complexes & Venues')
    st.dataframe(complex_venues_df)
    col1, col2 = st.columns(2)
    col1.metric("Total Complexes", complex_venues_df["complex_name"].nunique())
    col2.metric("Total Venues", complex_venues_df["venue_name"].nunique())


# 🔍 **Search & Filter Page (Custom Sidebar)**
elif selected_tab == "🔍 Search & Filter":
    st.sidebar.header("🎯 Search & Filter")

    search_name = st.sidebar.text_input("🔍 Search by Name", "")
    rank_range = st.sidebar.slider("📊 Filter by Rank", min_value=int(competitors_rankings_df["rank"].min()),
                                   max_value=int(competitors_rankings_df["rank"].max()),
                                   value=(1, 100))
    country_filter = st.sidebar.multiselect("🌍 Filter by Country", options=competitors_rankings_df["country"].unique())
    points_threshold = st.sidebar.slider("🔥 Filter by Points", min_value=int(competitors_rankings_df["points"].min()),
                                         max_value=int(competitors_rankings_df["points"].max()),
                                         value=int(competitors_rankings_df["points"].median()))

    # Apply filters
    filtered_df = competitors_rankings_df[
        (competitors_rankings_df["name"].str.contains(search_name, case=False, na=False)) &
        (competitors_rankings_df["rank"].between(rank_range[0], rank_range[1])) &
        (competitors_rankings_df["points"] >= points_threshold)
        ]

    if country_filter:
        filtered_df = filtered_df[filtered_df["country"].isin(country_filter)]

    st.subheader("🔍 Filtered Competitors")
    st.dataframe(filtered_df)

# 📊 **Competitor Details (Different Sidebar)**
elif selected_tab == "📊 Competitor Details":
    st.sidebar.header("📌 Competitor Details")
    selected_competitor = st.sidebar.selectbox("Select Competitor", competitors_rankings_df["name"].unique())

    competitor_info = competitors_rankings_df[competitors_rankings_df["name"] == selected_competitor]
    st.subheader(f"📊 Details for {selected_competitor}")
    st.dataframe(competitor_info)

# 🌍 **Country-Wise Analysis (Different Sidebar)**
elif selected_tab == "🌍 Country-Wise Analysis":
    st.sidebar.header("🌍 Country Analysis")
    selected_country = st.sidebar.selectbox("Select Country", competitors_rankings_df["country"].unique())

    country_stats = competitors_rankings_df[competitors_rankings_df["country"] == selected_country]
    st.subheader(f"🌍 Analysis for {selected_country}")
    st.dataframe(country_stats)

# 🏆 **Leaderboards (Different Sidebar)**
elif selected_tab == "🏆 Leaderboards":
    st.sidebar.header("🏆 Leaderboards")
    leaderboard_type = st.sidebar.radio("Select Leaderboard", ["Top 10 Ranked", "Top 5 Highest Points"])

    if leaderboard_type == "Top 10 Ranked":
        top_ranked = competitors_rankings_df.sort_values(by="rank", ascending=True).head(10)
        st.subheader("🏆 Top 10 Ranked Competitors")
        st.dataframe(top_ranked)

    elif leaderboard_type == "Top 5 Highest Points":
        highest_points = competitors_rankings_df.sort_values(by="points", ascending=False).head(5)
        st.subheader("🔥 Top 5 Competitors with Highest Points")
        st.dataframe(highest_points)
