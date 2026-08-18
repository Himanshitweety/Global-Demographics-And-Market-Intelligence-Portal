import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('world_population_by_country_2026.csv')

st.set_page_config(page_title="World Population Explorer", layout="wide")
st.title("World Population Explorer 2026")
st.markdown("Explore global demographic data across 233 countries.")

tab1 , tab2 , tab3 ,tab4, tab5 = st.tabs([
    "Global Overview",
    "World Map",
    "Country Deep Dive",
    "Country Comparison",
    "Market Opportunity"
])

# SIDEBAR FILTERS
st.sidebar.header("🔧 Filters")

# Population filter
min_pop = st.sidebar.slider(
    "Minimum Population",
    min_value=0,
    max_value=int(df["Population_2026"].max()),
    value=0,
    step=1000000,
    format="%d"
)

# Fertility rate filter
max_fertility = st.sidebar.slider(
    "Max Fertility Rate",
    min_value=float(df["Fertility_Rate"].min()),
    max_value=float(df["Fertility_Rate"].max()),
    value=float(df["Fertility_Rate"].max()),
    step=0.1
)

# Median age filter
min_age = st.sidebar.slider(
    "Minimum Median Age",
    min_value=float(df["Median_Age"].min()),
    max_value=float(df["Median_Age"].max()),
    value=float(df["Median_Age"].min()),
    step=0.5
)

# Urban population filter
min_urban = st.sidebar.slider(
    "Minimum Urban Population %",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

# Apply all filters
df_filtered = df[
    (df["Population_2026"] >= min_pop) &
    (df["Fertility_Rate"] <= max_fertility) &
    (df["Median_Age"] >= min_age) &
    (df["Urban_Population_pct"] >= min_urban)
]

# Show how many countries match
st.sidebar.metric("Countries matching", len(df_filtered))
st.sidebar.dataframe(
    df_filtered[["Country", "Population_2026"]].reset_index(drop=True),
    use_container_width=True
)

# TAB 1 — Global Overview

with tab1:
    st.header("Global Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Countries", len(df_filtered))
    with col2:
        world_pop = df_filtered["Population_2026"].sum()
        st.metric("World Population", f"{world_pop:,.0f}")
    with col3:
        avg_fertility = df_filtered["Fertility_Rate"].mean()
        st.metric("Avg Fertility Rate", f"{avg_fertility:.2f}")
    with col4:
        avg_age = df_filtered["Median_Age"].mean()
        st.metric("Avg Median Age", f"{avg_age:.1f}")

    st.divider()

    # Top 10 Most Populated
    st.subheader("Top 10 Most Populated Countries")
    top10 = df_filtered.nlargest(10, "Population_2026")[["Country", "Population_2026"]]
    

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.barh(top10["Country"], top10["Population_2026"], color="steelblue")
    ax1.set_xlabel("Population")
    ax1.set_title("Top 10 Countries by Population 2026")
    ax1.invert_yaxis()
    st.pyplot(fig1)
    plt.close()

    st.divider()

    # Top 10 Fastest Growing
    st.subheader("Top 10 Fastest Growing Countries")
    fastest = df_filtered.nlargest(10, "Yearly_Change")[["Country", "Yearly_Change"]]
   
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.barh(fastest["Country"], fastest["Yearly_Change"], color="green")
    ax2.set_xlabel("Yearly Change %")
    ax2.set_title("Top 10 Fastest Growing Countries")
    ax2.invert_yaxis()
    st.pyplot(fig2)
    plt.close()

    st.divider()

    st.divider()

