from __future__ import annotations

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from statsmodels.tsa.statespace.sarimax import SARIMAX

st.set_page_config(page_title="Ecobici BI | Pronóstico y Rebalanceo", layout="wide")

st.title("Pronóstico y Rebalanceo de Estaciones")

st.write("""
Este módulo permite generar pronósticos de bicicletas disponibles por estación
y sugerir movimientos de bicicletas entre estaciones para mantener un balance
operativo en el sistema Ecobici.
""")

if "station_data" not in st.session_state:
    st.info("Primero carga `station_data.csv` en la página principal.")
    st.stop()

station_data = st.session_state["station_data"]
static_stations = st.session_state.get("static_stations")

station_ids = sorted(station_data["station_id"].unique())


# -----------------------------------
# FUNCION PRONOSTICO
# -----------------------------------

def arima_forecast_station(station_id:int, freq="1H", horizon=24):

    df = station_data[station_data["station_id"] == station_id].copy()
    df = df.sort_values("timestamp")

    ts = (
        df.set_index("timestamp")["num_bikes_available"]
        .resample(freq)
        .mean()
        .interpolate(limit_direction="both")
    )

    seasonal_period = 24

    model = SARIMAX(
        ts,
        order=(1,1,1),
        seasonal_order=(1,0,1,seasonal_period),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    res = model.fit(disp=False)

    fc = res.get_forecast(steps=horizon)

    fc_mean = fc.predicted_mean
    fc_ci = fc.conf_int()

    return ts, fc_mean, fc_ci


# -----------------------------------
# FUNCION REBALANCEO
# -----------------------------------

def suggest_rebalancing_moves(target_ratio=0.5, buffer=2, top_moves=30):

    snap = (
        station_data.sort_values("timestamp")
        .groupby("station_id")
        .tail(1)
        .copy()
    )

    if static_stations is not None and "capacity" in static_stations.columns:

        cap = static_stations[["station_id","capacity"]].copy()
        cap["station_id"] = cap["station_id"].astype(int)

        snap = snap.merge(cap,on="station_id",how="left")

        if "capacity" in snap.columns:
            snap["capacity_final"] = snap["capacity"]
        elif "capacity_est" in snap.columns:
            snap["capacity_final"] = snap["capacity_est"]
        else:
            snap["capacity_final"] = snap["num_bikes_available"]


    snap["desired_bikes"] = (snap["capacity_final"] * target_ratio).round().astype(int)

    snap["delta"] = snap["num_bikes_available"] - snap["desired_bikes"]


    donors = snap[snap["delta"] > buffer][["station_id","delta"]].sort_values("delta",ascending=False)

    receivers = snap[snap["delta"] < -buffer][["station_id","delta"]].sort_values("delta")


    moves = []

    i = 0
    j = 0

    donors = donors.reset_index(drop=True)
    receivers = receivers.reset_index(drop=True)

    while i < len(donors) and j < len(receivers) and len(moves) < top_moves:

        donor_id = int(donors.loc[i,"station_id"])
        donor_surplus = int(donors.loc[i,"delta"])

        recv_id = int(receivers.loc[j,"station_id"])
        recv_deficit = int(-receivers.loc[j,"delta"])

        qty = min(donor_surplus,recv_deficit)

        moves.append({
            "De estación":donor_id,
            "A estación":recv_id,
            "Cantidad":qty
        })

        donors.loc[i,"delta"] -= qty
        receivers.loc[j,"delta"] += qty

        if donors.loc[i,"delta"] <= buffer:
            i += 1

        if receivers.loc[j,"delta"] >= -buffer:
            j += 1


    moves_df = pd.DataFrame(moves)

    if not moves_df.empty:

        moves_df["Instrucción"] = moves_df.apply(
            lambda x: f"Mover {x['Cantidad']} bicicletas de estación {x['De estación']} a estación {x['A estación']}",
            axis=1
        )

    return moves_df


# -----------------------------------
# SIDEBAR CONTROLES
# -----------------------------------

with st.sidebar:

    st.header("Parámetros de Pronóstico")

    station_id = st.selectbox("Estación",station_ids)

    freq = st.selectbox(
        "Frecuencia",
        ["30min","1H","2H"],
        index=1
    )

    horizon = st.slider(
        "Horas a pronosticar",
        6,
        72,
        24,
        step=6
    )

    st.header("Parámetros de Rebalanceo")

    target_ratio = st.slider(
        "Ratio objetivo de bicicletas",
        0.1,
        0.7,
        0.5,
        step=0.05
    )

    buffer = st.slider(
        "Buffer de tolerancia",
        0,
        10,
        2
    )

    top_moves = st.slider(
        "Máximo número de movimientos",
        5,
        100,
        30,
        step=5
    )


run = st.button("Generar pronóstico y sugerencias")


# -----------------------------------
# EJECUCION
# -----------------------------------

if run:

    ts, fc_mean, fc_ci = arima_forecast_station(
        station_id=int(station_id),
        freq=freq,
        horizon=horizon
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ts.index,
            y=ts.values,
            name="Datos históricos"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fc_mean.index,
            y=fc_mean.values,
            name="Pronóstico"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fc_ci.index,
            y=fc_ci.iloc[:,0],
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fc_ci.index,
            y=fc_ci.iloc[:,1],
            fill="tonexty",
            name="Intervalo de confianza"
        )
    )

    fig.update_layout(
        title=f"Pronóstico de bicicletas disponibles — estación {station_id}",
        xaxis_title="Fecha",
        yaxis_title="Bicicletas disponibles"
    )

    st.plotly_chart(fig,use_container_width=True)


    st.subheader("Sugerencias de rebalanceo")

    moves = suggest_rebalancing_moves(
        target_ratio=target_ratio,
        buffer=buffer,
        top_moves=top_moves
    )

    if moves.empty:

        st.success("No se requieren movimientos de bicicletas.")

    else:

        st.dataframe(moves,use_container_width=True)
