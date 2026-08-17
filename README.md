# 🌍 Global Demographics & Market Intelligence Portal

##  Project Overview
This interactive web application processes up-to-date global demographic metrics (Total Population, Median Age, and Urban Population %) to uncover market expansion opportunities. Built with Python and Streamlit, the portal cleans raw data, clusters nations using Machine Learning, and presents insights across a structured 3-tab layout.

---

##  Key Features & App Structure

* **Data Cleaning & Pipeline:**
  * Cleaned raw demographic data using Pandas by removing special characters (`%`, commas), converting text to numeric values, and handling missing values (`NaN`).
  * Scaled feature metrics using Scikit-Learn's `MinMaxScaler` for uniform model input.

* **Tab 1: Global Market Simulator & Clusters**
  * **K-Means Clustering:** Automatically groups countries into 4 distinct demographic archetypes based on age and urbanization.
  * **Interactive Choropleth Map:** Color-coded global visual analysis powered by Plotly Express.
  * **Custom Opportunity Scoring:** Dynamic Streamlit sliders allow users to set preferences (e.g., target younger workforce or higher urbanization) using a custom NumPy matrix scoring formula.

* **Tab 2: Country Deep-Dive**
  * **Interactive Selector:** Choose any individual country to view its stats instantly.
  * **Key Metric Cards:** Displays Total Population, Median Age, Urban Pop %, and assigned Cluster Group using Streamlit metrics.
  * **Benchmark Visuals:** Bar charts comparing the selected country's metrics directly against global averages.

* **Tab 3: Side-by-Side Country Comparison**
  * Select 2 or more countries to run comparative visual analyses across key demographic metrics.

---

## Tech Stack
* **Language:** Python
* **Data Handling & Math:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`KMeans`, `MinMaxScaler`)
* **Data Visualization:** Plotly Express
* **Web Framework:** Streamlit
A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

Prerequisite: install `uv` if you don't already have it.

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Sync the dependencies

   ```
   $ uv sync
   ```

2. Run the app

   ```
   $ uv run streamlit run streamlit_app.py
   ```
