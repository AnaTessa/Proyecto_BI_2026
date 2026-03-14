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
Modelo ARIMA con validación temporal, métricas e intervalos de confianza.
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

with st.sidebar:

    st.header("Parámetros")

    station_id = st.selectbox("station_id", station_ids)

    metric_label = st.selectbox(
        "Métrica",
        list(metric_map.keys())
    )

    resample = st.selectbox(
        "Frecuencia",
        ["30min", "1H", "1D"],
        index=1
    )

    p = st.slider("p",0,5,1)
    d = st.slider("d",0,2,1)
    q = st.slider("q",0,5,1)

    horizon = st.slider("Horizonte forecast",6,96,24)

col = metric_map[metric_label]

_df = sd[
    (sd["station_id"] == int(station_id))
].sort_values("timestamp")

series = (
    _df
    .set_index("timestamp")[col]
    .dropna()
    .resample(resample)
    .mean()
    .interpolate()
)

if len(series) < 50:
    st.warning("Serie demasiado corta")
    st.stop()

# Train/Test split
split = int(len(series)*0.8)

train = series[:split]
test = series[split:]

run = st.button("Entrenar modelo")

if run:

    with st.spinner("Entrenando ARIMA..."):

        model = ARIMA(train, order=(p,d,q))
        results = model.fit()

        forecast_test = results.forecast(len(test))

        # Métricas manuales
        mae = np.mean(np.abs(test.values - forecast_test))

        rmse = np.sqrt(
            np.mean((test.values - forecast_test)**2)
        )

        # Forecast futuro
        fc = results.get_forecast(steps=horizon)

        fc_mean = fc.predicted_mean
        fc_conf = fc.conf_int()

        fc_index = pd.date_range(
            series.index[-1],
            periods=horizon+1,
            freq=resample
        )[1:]

    col1,col2 = st.columns(2)

    col1.metric("MAE",round(mae,2))
    col2.metric("RMSE",round(rmse,2))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=train.index,
            y=train.values,
            name="Train"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=test.index,
            y=test.values,
            name="Test"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=test.index,
            y=forecast_test,
            name="Test Forecast"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fc_index,
            y=fc_mean,
            name="Future Forecast"
        )
    )

    # Intervalo de confianza
    fig.add_trace(
        go.Scatter(
            x=fc_index,
            y=fc_conf.iloc[:,0],
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fc_index,
            y=fc_conf.iloc[:,1],
            fill='tonexty',
            name="Confidence Interval"
        )
    )

    fig.update_layout(
        title=f"ARIMA({p},{d},{q}) – {metric_label}",
        xaxis_title="Time",
        yaxis_title=metric_label
    )

    st.plotly_chart(fig, use_container_width=True)
