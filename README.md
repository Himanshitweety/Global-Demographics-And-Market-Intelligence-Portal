World Population Explorer 2026

An interactive demographic dashboard built with Python and Streamlit that allows users to explore population data across 233 countries, identify market opportunities, and analyse global trends using machine learning.

Overview

This application takes a real-world dataset of global population statistics and transforms it into a five-tab interactive tool. Each tab answers a different question about the world's demographics — from basic exploration to machine learning powered market analysis.

Tabs
Tab 1 — Global Overview

The main landing page of the application. It displays four key metrics at the top — total countries, world population, average fertility rate, and average median age. Below that, two bar charts show the top 10 most populated countries and the top 10 fastest growing countries by yearly percentage change.

A sidebar with four sliders lets users filter the entire dataset in real time by minimum population, maximum fertility rate, minimum median age, and minimum urban population percentage. All charts and metrics update instantly when filters are changed. Users can also download the filtered or full dataset as a CSV file.

Tab 2 — World Map

An interactive map built with Folium showing the top 20 most populated countries as circular markers. The size of each circle is proportional to the country's population. Clicking any circle opens a popup showing the country's name, population, fertility rate, and median age. This tab gives users a geographic view of where population is concentrated globally.

Tab 3 — Country Deep Dive

Users select any country from a dropdown and instantly see its complete demographic profile across four metric cards — population, median age, urban population percentage, and fertility rate. A grouped bar chart below compares the selected country's key metrics against global averages, making it easy to see where a country stands relative to the rest of the world.

Tab 4 — Country Comparison

Users select two or more countries to compare side by side. A population bar chart shows the size difference between selected countries. Two smaller charts compare fertility rate and median age. A detailed table at the bottom displays all key metrics for the selected countries together in one view.

Tab 5 — Market Opportunity Analyser

The most advanced section of the application. Users set four preference sliders representing how much they value a young population, high urbanisation, fast population growth, and large market size. The application then scores all 233 countries using a weighted formula — each metric is normalised using Scikit-learn's MinMaxScaler so that no single metric dominates the score unfairly. The weighted scores are combined and scaled to a range of 0 to 100.

The top 10 countries by opportunity score are displayed as a bar chart. Users can also search for any specific country to see its score, a verdict label, its global rank out of 233, and a breakdown chart showing how much each factor contributed to its final score.

K-Means Clustering

Integrated into Tab 1, this unsupervised machine learning model automatically groups all 233 countries into four demographic clusters based on median age, urbanisation, fertility rate, and yearly growth. The clusters are labelled Young and Growing, Aging and Urban, Transitioning, and High Density. A pie chart shows the distribution and users can explore which countries fall into each cluster.

Technology Stack
Python
Streamlit
Pandas
NumPy
Matplotlib
Scikit-learn
Folium and Streamlit-Folium

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

How to Run
Option 1 — Run on Streamlit Cloud

Click the badge at the top of this README to open the live app directly in your browser.

Option 2 — Run locally using uv

Prerequisite: install uv if you don't already have it.

$ curl -LsSf https://astral.sh/uv/install.sh | sh
Sync the dependencies:
   $ uv sync
Run the app:
   $ uv run streamlit run streamlit_app.py
Option 3 — Run locally using pip
Install dependencies:
   $ pip install -r requirements.txt
Run the app:
   $ streamlit run streamlit_app.py
Open your browser and go to:
   http://localhost:8501
