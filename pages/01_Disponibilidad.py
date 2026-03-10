from __future__ import annotations

import streamlit as st

from src.kpis import distribution_availability, hourly_availability
from src.plots import fig_box_availability, fig_hourly_availability

st.set_page_config(page_title="Ecobici BI | Disponibilidad", layout="wide")

st.title("Disponibilidad")
st.write("Gráficas de disponibilidad por hora y distribución por estación.")

if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

station_data = st.session_state["station_data"]

# Filters
with st.sidebar:
    st.header("Filtros")
    installed_only = st.checkbox("Solo estaciones instaladas", value=True, key="avail_installed")

    min_date = station_data["timestamp"].min().date()
    max_date = station_data["timestamp"].max().date()

    date_range = st.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="avail_dates",
    )

    hour_range = st.slider("Rango de horas", 0, 23, (0, 23), key="avail_hours")

# Apply filters
_df = station_data

if installed_only and "is_installed" in _df.columns:
    _df = _df[_df["is_installed"]]

# date_range can return a single date if user clicks one day
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_range, date_range

_df = _df[(_df["date"] >= start_date) & (_df["date"] <= end_date)]
_df = _df[_df["hour"].between(hour_range[0], hour_range[1])]

# Charts
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Disponibilidad promedio por hora")
    h = hourly_availability(_df)
    st.plotly_chart(fig_hourly_availability(h), use_container_width=True)

with c2:
    st.subheader("Distribución (boxplot)")
    long_df = distribution_availability(_df)
    st.plotly_chart(fig_box_availability(long_df), use_container_width=True)

st.markdown("---")

st.subheader("Tabla de datos muestra (50)")
st.dataframe(_df.head(50), use_container_width=True)
