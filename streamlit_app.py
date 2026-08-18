import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('world_population_by_country_2026.csv')

st.set_page_config(page_title="World Population Explorer", layout="wide")
st.title("World Population Explorer 2026")
st.markdown("Explore global demographic data across 233 countries.")

