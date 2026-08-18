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
    # k -means clustering 

    st.subheader("Country Demographic Clusters")


    st.markdown("Countries automatically grouped by demographic similarity using K-Means.")

    from sklearn.preprocessing import MinMaxScaler
    from sklearn.cluster import KMeans


# Features for clustering
    cluster_features = ["Median_Age", "Urban_Population_pct",
                        "Fertility_Rate", "Yearly_Change"]
    cluster_data = df[cluster_features].copy()


# Scale the data — important for K-Means
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(cluster_data)

# Apply K-Means — 4 clusters
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(scaled_data)

    cluster_labels = {
        0: "🟢 Young & Growing",
        1: "🔵 Aging & Urban",
        2: "🟡 Transitioning",
        3: "🔴 High Density"
    }
    df["Cluster_Label"] = df["Cluster"].map(cluster_labels)
    # Show cluster distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cluster Distribution")
        cluster_counts = df["Cluster_Label"].value_counts()
        fig_cluster, ax_cluster = plt.subplots(figsize=(6, 4))
        ax_cluster.pie(
            cluster_counts.values,
            labels=cluster_counts.index,
            autopct="%1.1f%%",
            colors=["#2ecc71", "#3498db", "#f1c40f", "#e74c3c"]
            )
        ax_cluster.set_title("Countries by Cluster")
        st.pyplot(fig_cluster)
        plt.close()

    with col2:
        st.subheader("Cluster Summary")
        summary = df.groupby("Cluster_Label")[cluster_features].mean().round(2)
        st.dataframe(summary, use_container_width=True)

    st.divider()

    # Show countries per cluster
    selected_cluster = st.selectbox(
        "Explore a cluster",
        df["Cluster_Label"].unique()
    )
    cluster_countries = df[df["Cluster_Label"] == selected_cluster][
        ["Country", "Median_Age", "Urban_Population_pct",
         "Fertility_Rate", "Yearly_Change", "Population_2026"]
         ].sort_values("Population_2026", ascending=False)
    st.dataframe(cluster_countries, use_container_width=True)
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
# TAB 3 — Country Deep Dive
with tab3:
    st.header("Country Deep Dive")

    country = st.selectbox("Select a Country", df["Country"].sort_values())
    row = df[df["Country"] == country].iloc[0]

    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Population 2026", f"{row['Population_2026']:,.0f}")
    with col2:
        st.metric("Median Age", f"{row['Median_Age']}")
    with col3:
        st.metric("Urban Population %", f"{row['Urban_Population_pct']}%")
    with col4:
        st.metric("Fertility Rate", f"{row['Fertility_Rate']}")

    st.divider()

    # Benchmark chart
    st.subheader(f"📊 {country} vs World Average")
    metrics = ["Fertility_Rate", "Median_Age", "Urban_Population_pct", "Density_per_km2"]
    world_avg = df[metrics].mean()
    country_vals = [row[m] for m in metrics]
    avg_vals = [world_avg[m] for m in metrics]

    x = range(len(metrics))
    width = 0.35

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.bar([i - width/2 for i in x], country_vals, width, label=country, color="steelblue")
    ax3.bar([i + width/2 for i in x], avg_vals, width, label="World Avg", color="orange")
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(metrics, rotation=15)
    ax3.legend()
    ax3.set_title(f"{country} vs World Average")
    st.pyplot(fig3)
    plt.close()

# tab 4 

with tab4:
    st.header("Side-by-Side Country Comparison")

    selected = st.multiselect(
        "Select 2 or more countries",
        df["Country"].sort_values(),
        default=["India", "China", "United States"]
    )

    if len(selected) < 2:
        st.warning("Please select at least 2 countries.")
    else:
        filtered = df[df["Country"].isin(selected)]

        st.divider()

        # Population comparison
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.bar(filtered["Country"], filtered["Population_2026"], color="steelblue")
        ax4.set_title("Population Comparison")
        ax4.set_ylabel("Population")
        plt.xticks(rotation=15)
        st.pyplot(fig4)
        plt.close()

        col1, col2 = st.columns(2)

        with col1:
            fig5, ax5 = plt.subplots(figsize=(6, 4))
            ax5.bar(filtered["Country"], filtered["Fertility_Rate"], color="green")
            ax5.set_title("Fertility Rate")
            plt.xticks(rotation=15)
            st.pyplot(fig5)
            plt.close()

        with col2:
            fig6, ax6 = plt.subplots(figsize=(6, 4))
            ax6.bar(filtered["Country"], filtered["Median_Age"], color="orange")
            ax6.set_title("Median Age")
            plt.xticks(rotation=15)
            st.pyplot(fig6)
            plt.close()

        # Comparison table
        st.subheader("📋 Detailed Comparison Table")
        st.dataframe(
            filtered[["Country", "Population_2026", "Yearly_Change",
                      "Fertility_Rate", "Median_Age",
                      "Urban_Population_pct", "World_Share_pct"]].set_index("Country"),
            use_container_width=True
        )

with tab5:
    st.header("Market Opportunity Analyser")
    st.markdown("Set your business preferences and discover the best countries to expand into.")

    st.divider()

    # --- User Preferences ---
    st.subheader("Set Your Business Preferences")
    st.markdown("Move the sliders to match what matters most for your business.")

    col1, col2 = st.columns(2)

    with col1:
        w_young = st.slider(
            "Young Population Matters",
            0.0, 1.0, 0.5, 0.1,
            help="Higher = prefer countries with younger median age"
        )
        w_urban = st.slider(
            "Urban Population Matters",
            0.0, 1.0, 0.5, 0.1,
            help="Higher = prefer countries with more urban population"
        )

    with col2:
        w_growth = st.slider(
            "Population Growth Matters",
            0.0, 1.0, 0.5, 0.1,
            help="Higher = prefer fast growing markets"
        )
        w_size = st.slider(
            "Market Size Matters",
            0.0, 1.0, 0.5, 0.1,
            help="Higher = prefer larger population markets"
        )

    st.divider()

    # --- Scoring Logic ---
    from sklearn.preprocessing import MinMaxScaler
    import numpy as np

    score_df = df.copy()

    # Normalise each metric to 0-1
    scaler = MinMaxScaler()
    score_df["norm_young"] = 1 - scaler.fit_transform(
        score_df[["Median_Age"]])          # invert — younger = higher score
    score_df["norm_urban"] = scaler.fit_transform(
        score_df[["Urban_Population_pct"]])
    score_df["norm_growth"] = scaler.fit_transform(
        score_df[["Yearly_Change"]])
    score_df["norm_size"] = scaler.fit_transform(
        score_df[["Population_2026"]])

    # Calculate weighted opportunity score
    score_df["Opportunity_Score"] = (
        w_young  * score_df["norm_young"] +
        w_urban  * score_df["norm_urban"] +
        w_growth * score_df["norm_growth"] +
        w_size   * score_df["norm_size"]
    )

    # Scale score to 0-100
    score_df["Opportunity_Score"] = (
        score_df["Opportunity_Score"] /
        (w_young + w_urban + w_growth + w_size + 0.0001) * 100
    ).round(1)

    # --- Top 10 Opportunities ---
    st.subheader("Top 10 Market Opportunities")
    top_markets = score_df.nlargest(10, "Opportunity_Score")[
        ["Country", "Opportunity_Score", "Population_2026",
         "Median_Age", "Urban_Population_pct", "Yearly_Change"]
    ].reset_index(drop=True)

    # Bar chart
    fig_score, ax_score = plt.subplots(figsize=(10, 5))
    bars = ax_score.barh(
        top_markets["Country"],
        top_markets["Opportunity_Score"],
        color="steelblue"
    )
    ax_score.set_xlabel("Opportunity Score (0-100)")
    ax_score.set_title("Top 10 Countries by Market Opportunity")
    ax_score.invert_yaxis()

    # Add score labels on bars
    for bar, score in zip(bars, top_markets["Opportunity_Score"]):
        ax_score.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{score}",
            va="center",
            fontsize=9
        )

    st.pyplot(fig_score)
    plt.close()

    st.dataframe(top_markets, use_container_width=True)

    st.divider()

    # --- Single Country Check ---
    st.subheader("🔍 Check a Specific Country")
    check_country = st.selectbox(
        "Select a country to analyse",
        score_df["Country"].sort_values(),
        key="opportunity_country"
    )

    country_row = score_df[score_df["Country"] == check_country].iloc[0]
    score = country_row["Opportunity_Score"]

    # Score colour
    if score >= 70:
        colour = "🟢"
        verdict = "Excellent opportunity!"
    elif score >= 50:
        colour = "🟡"
        verdict = "Moderate opportunity"
    elif score >= 30:
        colour = "🟠"
        verdict = "Low opportunity"
    else:
        colour = "🔴"
        verdict = "Not recommended"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Opportunity Score", f"{score}/100")
    with col2:
        st.metric("Verdict", f"{colour} {verdict}")
    with col3:
        rank = score_df["Opportunity_Score"].rank(ascending=False)[
            score_df["Country"] == check_country].values[0]
        st.metric("Global Rank", f"#{int(rank)} of 233")

    st.divider()

    # Breakdown chart — why this score
    st.subheader(f"Score Breakdown — {check_country}")

    breakdown_labels = ["Young Population", "Urban Population",
                        "Growth Rate", "Market Size"]
    breakdown_values = [
        round(w_young  * country_row["norm_young"]  * 100, 1),
        round(w_urban  * country_row["norm_urban"]  * 100, 1),
        round(w_growth * country_row["norm_growth"] * 100, 1),
        round(w_size   * country_row["norm_size"]   * 100, 1),
    ]

    fig_breakdown, ax_breakdown = plt.subplots(figsize=(8, 4))
    bars2 = ax_breakdown.bar(
        breakdown_labels,
        breakdown_values,
        color=["#2ecc71", "#3498db", "#f1c40f", "#e74c3c"]
    )
    ax_breakdown.set_ylabel("Score Contribution")
    ax_breakdown.set_title(f"What drives {check_country}'s score?")

    for bar, val in zip(bars2, breakdown_values):
        ax_breakdown.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"{val}",
            ha="center",
            fontsize=10
        )

    st.pyplot(fig_breakdown)
    plt.close()        