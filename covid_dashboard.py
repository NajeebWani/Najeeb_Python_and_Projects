# covid_dashboard.py
"""
COVID-19 Dashboard (Streamlit + Plotly)
- Fetches live data from Our World in Data
- Shows global summary, country metrics, timeseries charts and world map
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime

# ====== CONFIG ======
OWID_CSV_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide", initial_sidebar_state="expanded")

# ====== HELPERS / DATA LOADING ======
@st.cache_data(ttl=60*60)  # cache for 1 hour
def load_owid_data(url=OWID_CSV_URL):
    # Download CSV from OWID
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    s = StringIO(resp.text)
    df = pd.read_csv(s, parse_dates=["date"])
    return df

def filter_country(df, country):
    if country == "Global":
        return df.copy()
    return df[df["location"] == country].copy()

def compute_latest_metrics(df_country):
    # If df_country is global (multiple locations), aggregate by date first
    if df_country["location"].nunique() > 1:
        daily = df_country.groupby("date", as_index=False).agg({
            "new_cases": "sum", "new_deaths": "sum",
            "total_cases": "sum", "total_deaths": "sum",
            "people_vaccinated": "sum", "people_fully_vaccinated": "sum",
            "total_vaccinations": "sum", "population": "sum"
        })
        last = daily.sort_values("date").iloc[-1]
    else:
        daily = df_country.sort_values("date")
        last = daily.iloc[-1]
    return {
        "date": last["date"],
        "total_cases": int(last.get("total_cases", 0) or 0),
        "new_cases": int(last.get("new_cases", 0) or 0),
        "total_deaths": int(last.get("total_deaths", 0) or 0),
        "new_deaths": int(last.get("new_deaths", 0) or 0),
        "total_vaccinations": int(last.get("total_vaccinations", 0) or 0),
        "people_vaccinated": int(last.get("people_vaccinated", 0) or 0),
        "population": int(last.get("population", 0) or 0)
    }

def rolling_mean(series, window):
    return series.rolling(window=window, min_periods=1, center=False).mean()

# ====== APP LAYOUT ======
st.title("🌍 COVID-19 Interactive Dashboard")
st.markdown("Data source: Our World in Data — updated live from `owid-covid-data.csv`")

# Load data
with st.spinner("Loading data from Our World in Data..."):
    df = load_owid_data()

# Sidebar controls
st.sidebar.header("Controls")
countries = ["Global"] + sorted(df["location"].unique().tolist())
selected_country = st.sidebar.selectbox("Select country", countries, index=0)
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)

per_million = st.sidebar.checkbox("Show per million (cases/deaths per 1M)", value=False)
smooth = st.sidebar.checkbox("Apply smoothing (7-day rolling average)", value=True)
smooth_window = st.sidebar.slider("Smoothing window (days)", min_value=3, max_value=14, value=7, step=1)
show_map = st.sidebar.checkbox("Show world map (choropleth)", value=True)
download_data = st.sidebar.button("Download filtered data (CSV)")

# Filter by country and date
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df_country = filter_country(df, selected_country)
df_country = df_country[(df_country["date"] >= start_date) & (df_country["date"] <= end_date)].sort_values("date")

# Top-level metrics
metrics = compute_latest_metrics(df_country if selected_country != "Global" else df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cases", f"{metrics['total_cases']:,}")
col2.metric("New Cases (latest)", f"{metrics['new_cases']:,}")
col3.metric("Total Deaths", f"{metrics['total_deaths']:,}")
col4.metric("New Deaths (latest)", f"{metrics['new_deaths']:,}")

st.markdown(f"**Latest data date:** {metrics['date'].date()}")

# Download filtered data
if download_data:
    csv = df_country.to_csv(index=False)
    st.download_button("Click to download CSV", data=csv, file_name=f"{selected_country}_covid_data.csv", mime="text/csv")

# Time-series charts
st.markdown("### Time Series")
ts_col1, ts_col2 = st.columns(2)

with ts_col1:
    # New/Total cases chart
    df_plot = df_country.copy()
    if per_million:
        # avoid division by zero
        df_plot["new_cases_per_mil"] = (df_plot["new_cases"] / df_plot["population"]) * 1_000_000
        df_plot["total_cases_per_mil"] = (df_plot["total_cases"] / df_plot["population"]) * 1_000_000
        y_new = "new_cases_per_mil"
        y_total = "total_cases_per_mil"
        y_title = "Cases per 1M"
    else:
        y_new = "new_cases"
        y_total = "total_cases"
        y_title = "Cases"

    if smooth:
        df_plot[y_new] = rolling_mean(df_plot[y_new].fillna(0), smooth_window)
        df_plot[y_total] = rolling_mean(df_plot[y_total].fillna(0), smooth_window)

    fig_cases = px.line(df_plot, x="date", y=[y_new, y_total],
                        labels={"value": y_title, "variable": "Series"},
                        title=f"New vs Total Cases — {selected_country}")
    fig_cases.update_layout(legend=dict(x=0, y=1.05, orientation="h"))
    st.plotly_chart(fig_cases, use_container_width=True)

with ts_col2:
    # New/Total deaths chart
    df_plot = df_country.copy()
    if per_million:
        df_plot["new_deaths_per_mil"] = (df_plot["new_deaths"] / df_plot["population"]) * 1_000_000
        df_plot["total_deaths_per_mil"] = (df_plot["total_deaths"] / df_plot["population"]) * 1_000_000
        y_new_d = "new_deaths_per_mil"
        y_total_d = "total_deaths_per_mil"
        y_title_d = "Deaths per 1M"
    else:
        y_new_d = "new_deaths"
        y_total_d = "total_deaths"
        y_title_d = "Deaths"

    if smooth:
        df_plot[y_new_d] = rolling_mean(df_plot[y_new_d].fillna(0), smooth_window)
        df_plot[y_total_d] = rolling_mean(df_plot[y_total_d].fillna(0), smooth_window)

    fig_deaths = px.line(df_plot, x="date", y=[y_new_d, y_total_d],
                         labels={"value": y_title_d, "variable": "Series"},
                         title=f"New vs Total Deaths — {selected_country}")
    fig_deaths.update_layout(legend=dict(x=0, y=1.05, orientation="h"))
    st.plotly_chart(fig_deaths, use_container_width=True)

# Vaccination chart (if available)
st.markdown("### Vaccinations")
if "people_vaccinated" in df_country.columns and df_country["people_vaccinated"].notna().any():
    df_vax = df_country.copy()
    if smooth:
        df_vax["people_vaccinated"] = rolling_mean(df_vax["people_vaccinated"].fillna(0), smooth_window)
        df_vax["people_fully_vaccinated"] = rolling_mean(df_vax["people_fully_vaccinated"].fillna(0), smooth_window)
    fig_vax = px.line(df_vax, x="date", y=["people_vaccinated", "people_fully_vaccinated"],
                      labels={"value": "People", "variable": "Series"},
                      title=f"People Vaccinated — {selected_country}")
    fig_vax.update_layout(legend=dict(x=0, y=1.05, orientation="h"))
    st.plotly_chart(fig_vax, use_container_width=True)
else:
    st.info("Vaccination data not available for the selected range/country.")

# Show table of the most recent rows
st.markdown("### Recent Data Snapshot")
if df_country.empty:
    st.warning("No data for the selected country/date range.")
else:
    st.dataframe(df_country.sort_values("date", ascending=False).head(10))

# Choropleth map
if show_map:
    st.markdown("### World Map — Total cases per country (latest available)")
    # Build latest-per-country snapshot
    df_latest = df.groupby("location", as_index=False).apply(lambda g: g.sort_values("date").iloc[-1]).reset_index(drop=True)
    # Filter out continents & aggregates which OWID includes like "World", "Asia" etc by requiring iso_code to be 3 letters
    df_latest = df_latest[df_latest["iso_code"].str.len() == 3]
    df_latest["total_cases_filled"] = df_latest["total_cases"].fillna(0)
    # Option: show per_million on map
    if per_million:
        df_latest["cases_per_mil"] = (df_latest["total_cases_filled"] / df_latest["population"]) * 1_000_000
        color_col = "cases_per_mil"
        color_title = "Total cases per 1M"
    else:
        color_col = "total_cases_filled"
        color_title = "Total cases"

    fig_map = px.choropleth(df_latest,
                            locations="iso_code",
                            color=color_col,
                            hover_name="location",
                            hover_data={"iso_code": False, "population": True, color_col: True},
                            color_continuous_scale="Reds",
                            labels={color_col: color_title},
                            title="World COVID-19 Choropleth (latest snapshot)")
    fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

# Footer / credits
st.markdown("---")
st.caption("Built with Streamlit • Data from Our World in Data (owid-covid-data.csv)")

