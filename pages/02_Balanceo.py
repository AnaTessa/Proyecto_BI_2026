from __future__ import annotations

import streamlit as st

from src.kpis import balance_by_day_of_week, station_service_levels
from src.plots import fig_balance_by_dow, fig_map_least_balanced

st.set_page_config(page_title="Ecobici BI | Balanceo", layout="wide")

st.title("Balanceo")


if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

station_data = st.session_state["station_data"]

# -----------------------------
# Balance ratio by day of week
# -----------------------------

st.subheader("Balance ratio por día")
dow_df = balance_by_day_of_week(station_data)
st.plotly_chart(fig_balance_by_dow(dow_df), use_container_width=True)

st.markdown("---")

# -----------------------------
# Least balanced map + table
# -----------------------------

st.subheader("Least balanced stations")

if "least_balanced" not in st.session_state:
    st.warning("No cargaste `least_balanced_stations.csv`. Ve a la página principal y cárgalo para ver el mapa.")
else:
    least = st.session_state["least_balanced"].copy()

    # Optional: enrich with service levels computed from station_data
    svc = station_service_levels(station_data)
    least = least.merge(svc, on="station_id", how="left", suffixes=("_least", "_dyn"))

    with st.sidebar:
        st.header("Mapa / tabla")
        top_n = st.slider("Mostrar top N (más desbalanceadas)", 5, min(100, len(least)), 25, step=5)
        st.write("""Sólo para la segunda gráfica.""")

    least_sorted = least.sort_values("balance_ratio", ascending=True).head(top_n)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.plotly_chart(fig_map_least_balanced(least_sorted), use_container_width=True)

    with c2:
        st.caption("Tabla (top estaciones menos balanceadas)")
        cols = [
            "station_id",
            "name",
            "balance_ratio",
            "capacity",
            "pct_has_bike",
            "pct_has_dock",
            "pct_has_both",
            "avg_bikes",
            "avg_docks",
            "avg_balance_ratio",
        ]
        cols = [c for c in cols if c in least_sorted.columns]
        st.dataframe(
            least_sorted[cols].reset_index(drop=True),
            use_container_width=True,
        )
