from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Ecobici BI | Forecast", layout="wide")

st.title("Pronóstico de estaciones Ecobici (SARIMA)")

st.write(
"""
Modelo de pronóstico usando SARIMA con validación temporal,
intervalos de confianza y métricas de error.
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

    st.subheader("ARIMA")

    p = st.slider("p",0,5,1)
    d = st.slider("d",0,2,1)
    q = st.slider("q",0,5,1)

    st.subheader("Seasonal")

    P = st.slider("P",0,3,1)
    D = st.slider("D",0,2,1)
    Q = st.slider("Q",0,3,1)

    if resample == "1H":
        s = 24
    elif resample == "30min":
        s = 48
    else:
        s = 7

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

split = int(len(series)*0.8)

train = series[:split]
test = series[split:]

run = st.button("Entrenar modelo")

if run:

    with st.spinner("Entrenando SARIMA..."):

        model = SARIMAX(
            train,
            order=(p,d,q),
            seasonal_order=(P,D,Q,s),
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        results = model.fit()

        forecast_test = results.forecast(len(test))

        mae = mean_absolute_error(test, forecast_test)

        rmse = np.sqrt(
            mean_squared_error(test, forecast_test)
        )

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
        title=f"SARIMA({p},{d},{q})({P},{D},{Q},{s}) – {metric_label}",
        xaxis_title="Time",
        yaxis_title=metric_label
    )

    st.plotly_chart(fig, use_container_width=True)
