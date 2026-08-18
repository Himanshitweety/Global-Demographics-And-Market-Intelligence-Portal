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
# Full table
    st.subheader("📋 Full Dataset")
    st.dataframe(
        df_filtered.sort_values("Rank")[["Rank", "Country", "Population_2026",
                                 "Yearly_Change", "Fertility_Rate",
                                 "Median_Age", "Urban_Population_pct"]],
        use_container_width=True
    )
    st.subheader("Download Data")

    col1, col2 = st.columns(2)
    with col1:
        csv_filtered = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data",
            data=csv_filtered,
            file_name="world_population_filtered.csv",
            mime="text/csv"
            )
    with col2:
        csv_full = df.to_csv(index=False)
        st.download_button(
            label="Download Full Dataset",
            data=csv_full,
            file_name="world_population_2026.csv",
            mime="text/csv"
            )
# tab 2 
with tab2:
    st.header("World Population Map")

    import folium
    from streamlit_folium import st_folium
    country_coords = {
        "India": [20.5937, 78.9629],
        "China": [35.8617, 104.1954],
        "United States": [37.0902, -95.7129],
        "Indonesia": [-0.7893, 113.9213],
        "Pakistan": [30.3753, 69.3451],
        "Nigeria": [9.0820, 8.6753],
        "Brazil": [-14.2350, -51.9253],
        "Bangladesh": [23.6850, 90.3563],
        "Russia": [61.5240, 105.3188],
        "Ethiopia": [9.1450, 40.4897],
        "Mexico": [23.6345, -102.5528],
        "Japan": [36.2048, 138.2529],
        "Philippines": [12.8797, 121.7740],
        "DR Congo": [-4.0383, 21.7587],
        "Egypt": [26.8206, 30.8025],
        "Vietnam": [14.0583, 108.2772],
        "Iran": [32.4279, 53.6880],
        "Turkey": [38.9637, 35.2433],
        "Germany": [51.1657, 10.4515],
        "Thailand": [15.8700, 100.9925],
    }

    m = folium.Map(location=[20, 0], zoom_start=2)

    for country, coords in country_coords.items():
        row = df[df["Country"] == country]
        if not row.empty:
            pop = int(row["Population_2026"].values[0])
            fertility = float(row["Fertility_Rate"].values[0])
            median_age = float(row["Median_Age"].values[0])

            # Size based on population
            radius = max(5, pop / 50000000)

            folium.CircleMarker(
                location=coords,
                radius=radius,
                color="steelblue",
                fill=True,
                fill_color="steelblue",
                fill_opacity=0.6,
                popup=folium.Popup(
                    f"""
                    <b>{country}</b><br>
                    Population: {pop:,}<br>
                    Fertility Rate: {fertility}<br>
                    Median Age: {median_age}
                    """,
                    max_width=200
                ),
                tooltip=country
            ).add_to(m)

    st_folium(m, width=1200, height=500)

    st.caption("Circle size represents relative population. Click any circle for details.")