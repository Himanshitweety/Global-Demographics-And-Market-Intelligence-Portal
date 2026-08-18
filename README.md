# World Population Explorer 2026

Live demo: https://global-demographics.streamlit.app/

A Python-based interactive analytics dashboard for exploring demographic patterns across 233 countries, benchmarking key indicators, and identifying market opportunities through data-driven scoring and clustering.

## Overview

This project uses a global population dataset to build a multi-tab Streamlit application for demographic analysis and strategic insight generation. The system combines exploratory visual analytics with machine learning to support market screening and country-level comparison.

### Core capabilities
- analyse demographic indicators such as population, fertility rate, median age, and urbanization
- compare countries across multiple dimensions in a single interface
- visualize geographic concentration through an interactive map
- evaluate opportunity potential using a weighted scoring model
- apply unsupervised clustering to identify similar demographic profiles

## Features

### 1. Global Overview
- KPI cards for total countries, total population, average fertility rate, and median age
- top 10 countries by population
- top 10 countries by yearly growth rate
- interactive filtering by population, fertility, age, and urban concentration
- CSV export for filtered or full dataset views

### 2. World Map
- Folium-based geographic visualization of high-population countries
- circular markers scaled by population size
- country-level summaries in map popups

### 3. Country Deep Dive
- country selector for granular demographic inspection
- metric cards for population, median age, urban population share, and fertility rate
- comparison against global averages for direct benchmarking

### 4. Country Comparison
- multi-country comparison across population, fertility, and median age
- comparative bar charts and summary tables
- quick identification of relative strengths and gaps

### 5. Market Opportunity Analyzer
- weighted scoring framework based on youth profile, urbanization, growth, and market size
- MinMax normalization to avoid metric dominance bias
- rank-based opportunity assessment on a 0–100 scale
- country-specific score breakdown and ranking information

### 6. K-Means Clustering
- demographic segmentation using K-Means clustering
- cluster labels such as Young & Growing, Aging & Urban, Transitioning, and High Density
- cluster distribution visualization and country-level cluster exploration

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly
- Scikit-learn
- Folium
- streamlit-folium

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## Project Structure

- `streamlit_app.py` — main Streamlit dashboard implementation
- `world_population_by_country_2026.csv` — demographic dataset used in the app
- `requirements.txt` — Python dependencies
- `pyproject.toml` — project metadata and uv configuration
- `README.md` — project documentation

## Run the Application

### Option 1: Streamlit Cloud
Click the badge above to launch the app in the browser.

### Option 2: Local setup with uv

Install uv if it is not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run:

```bash
uv sync
uv run streamlit run streamlit_app.py
```

### Option 3: Local setup with pip

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the app in your browser at:

```text
http://localhost:8501
```

