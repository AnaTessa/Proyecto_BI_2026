from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.kpis import disabled_by_day_of_week, top_disabled_stations
from src.plots import fig_disabled_by_dow, fig_top_disabled

st.set_page_config(page_title="Ecobici BI | Mantenimiento", layout="wide")

st.title("Mantenimiento")
st.write(
    """
Este módulo replica:
- Puedes revisar las estaciones con más bicis deshabilitadas totales o excluyendo 00:00–05:00.
"""
)

if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

sd = st.session_state["station_data"]

with st.sidebar:
    st.header("Parámetros")
    top_n = st.slider("Top N estaciones", 5, 50, 10, step=5)
    exclude_night = st.checkbox("Excluir 00:00–05:00", value=True)
    st.write(
    """
Sólo para la primera gráfica.
"""
)

start_hour = 5 if exclude_night else 0
end_hour = 23

# Top disabled
st.subheader("Hotspots de bicis deshabilitadas")
top_df = top_disabled_stations(sd, start_hour=start_hour, end_hour=end_hour, top_n=top_n)
st.plotly_chart(fig_top_disabled(top_df), use_container_width=True)


# By day of week
st.subheader("Deshabilitadas por día")
dow = disabled_by_day_of_week(sd)
st.plotly_chart(fig_disabled_by_dow(dow), use_container_width=True)

# Hourly profile
st.subheader("Perfil horario (deshabilitadas y renting)")

hourly = sd.groupby("hour").agg(
    avg_disabled=("num_bikes_disabled", "mean"),
    avg_bikes=("num_bikes_available", "mean"),
    avg_docks=("num_docks_available", "mean"),
)

if "is_renting" in sd.columns:
    hourly["renting_rate"] = sd.groupby("hour")["is_renting"].mean()

hourly = hourly.reset_index()

fig1 = px.line(hourly, x="hour", y="avg_disabled", markers=True, title="Average disabled bikes by hour")
fig1.update_xaxes(dtick=2)

st.plotly_chart(fig1, use_container_width=True)

if "renting_rate" in hourly.columns:
    fig2 = px.line(hourly, x="hour", y="renting_rate", markers=True, title="Renting rate by hour")
    fig2.update_yaxes(range=[0, 1])
    fig2.update_xaxes(dtick=2)
    st.plotly_chart(fig2, use_container_width=True)
