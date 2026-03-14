from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Ecobici BI | Pronóstico", layout="wide")

st.title("Pronóstico (ARIMA)")
st.write(
    """
Baseline de pronóstico por estación (similar a l realizado en el ipynb).
"""
)

if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

sd = st.session_state["station_data"]

station_ids = sorted(sd["station_id"].unique().tolist())
metric_map = {
    "Bikes available": "num_bikes_available",
    "Balance ratio": "balance_ratio",
}

@st.cache_resource(show_spinner=False)
def fit_arima(y: np.ndarray, order: tuple[int, int, int]):
    # statsmodels expects 1D array-like
    model = ARIMA(y, order=order)
    res = model.fit()
    return res

with st.sidebar:
    st.header("Parámetros")
    station_id = st.selectbox("station_id", station_ids, index=0)
    metric_label = st.selectbox("Métrica", list(metric_map.keys()), index=0)
    resample = st.selectbox("Resample", ["30min", "1H", "1D"], index=1)

    p = st.slider("p", 0, 5, 1)
    d = st.slider("d", 0, 2, 1)
    q = st.slider("q", 0, 5, 1)

    horizon = st.slider("Horizonte (pasos)", 6, 96, 24, step=6)

col = metric_map[metric_label]

_df = sd[(sd["station_id"] == int(station_id)) & (sd.get("is_installed", True))].sort_values("timestamp")

s = _df.set_index("timestamp")[col].dropna()

# Resample to regular frequency
s = s.resample(resample).mean().interpolate(limit_direction="both")

if len(s) < 30:
    st.warning("Serie demasiado corta para ARIMA con parámetros actuales. Elige otra estación o mayor granularidad.")
    st.stop()

# Fit + forecast
order = (p, d, q)

run = st.button("Entrenar y pronosticar")

if run:
    with st.spinner("Entrenando ARIMA..."):
        y = s.astype(float).to_numpy()
        model = fit_arima(y, order)
        yhat = model.forecast(steps=horizon)

    # Build forecast index
    last_ts = s.index[-1]
    freq = pd.tseries.frequencies.to_offset(resample)
    fc_index = pd.date_range(last_ts + freq, periods=horizon, freq=freq)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines", name="Actual"))
    fig.add_trace(go.Scatter(x=fc_index, y=yhat, mode="lines", name="Forecast"))
    fig.update_layout(title=f"ARIMA{order} – {metric_label} – station_id={station_id}")

    st.plotly_chart(fig, use_container_width=True)
