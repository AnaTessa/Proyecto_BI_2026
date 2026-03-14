from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Ecobici BI | Drill-down", layout="wide")

st.title("Drill-down por estación")
st.write("Explora una estación específica: serie de tiempo + KPIs de nivel de servicio.")

if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

sd = st.session_state["station_data"]

station_ids = sorted(sd["station_id"].unique().tolist())
metric_map = {
    "Bikes available": "num_bikes_available",
    "Docks available": "num_docks_available",
    "Bikes disabled": "num_bikes_disabled",
    "Docks disabled": "num_docks_disabled",
    "Balance ratio": "balance_ratio",
}

with st.sidebar:
    st.header("Selección")
    station_id = st.selectbox("station_id", station_ids, index=0)
    metric_label = st.selectbox("Métrica", list(metric_map.keys()), index=0)
    resample = st.selectbox("Resample", ["30min", "1H", "1D"], index=2)

col = metric_map[metric_label]

_df = sd[sd["station_id"] == int(station_id)].sort_values("timestamp")

# Basic KPIs
has_bike = (_df["num_bikes_available"] >= 1).mean()
has_dock = (_df["num_docks_available"] >= 1).mean()
has_both = ((_df["num_bikes_available"] >= 1) & (_df["num_docks_available"] >= 1)).mean()

c1, c2, c3 = st.columns(3)
c1.metric("% con >=1 bici", f"{has_bike*100:.1f}%")
c2.metric("% con >=1 dock", f"{has_dock*100:.1f}%")
c3.metric("% con ambos", f"{has_both*100:.1f}%")

# Time series
s = _df.set_index("timestamp")[col]

plot_df = s.reset_index().rename(columns={0: col, col: "value"})
fig = px.line(plot_df, x="timestamp", y="value", title=f"{metric_label} – station_id={station_id}")

st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver datos de la estación"):
    st.dataframe(_df.head(200), use_container_width=True)
