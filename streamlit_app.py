from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.loaders import (
    load_least_balanced_from_path,
    load_station_data_from_path,
    load_static_stations_from_path,
    load_trips_from_path,
)
from src.kpis import kpi_basic_health

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

st.set_page_config(page_title="Ecobici BI", layout="wide")

st.title("Ecobici BI Dashboard")
st.write(
    """
Este dashboard replica y extiende el análisis del archivo ipynb y la presentación.

**Cómo usarlo:**
- Carga los CSV desde el repositorio (`data/`)
- Navega por las páginas (sidebar) para ver los gráficos.

Archivos utilizados:
- `station_data.csv` 
- `least_balanced_stations.csv`
- `static_stations.csv`
- `eco_bici_trips.csv`
- `eco_bici_trips_s.csv`
"""
)

# -----------------------------
# Sidebar: load data
# -----------------------------

st.sidebar.header("1) Carga de datos")
mode = st.sidebar.radio(
    "Fuente de datos",
    ["Usar archivos del repo (data/)"],
)

# Helper to show state

def _has(key: str) -> bool:
    return key in st.session_state and st.session_state[key] is not None


if mode == "Usar archivos del repo (data/)":
    st.sidebar.caption("Se usan los CSV en la carpeta `data/`.")

    station_path = DATA_DIR / "station_data.csv"
    least_path = DATA_DIR / "least_balanced_stations.csv"
    static_path = DATA_DIR / "static_stations.csv"
    trips_path = DATA_DIR / "eco_bici_trips.csv"
    trips_s_path = DATA_DIR / "eco_bici_trips_s.csv"

    if station_path.exists():
        st.session_state["station_data"] = load_station_data_from_path(str(station_path))
        st.sidebar.success("station_data.csv cargado")
    else:
        st.sidebar.error("Falta data/station_data.csv")

    if least_path.exists():
        st.session_state["least_balanced"] = load_least_balanced_from_path(str(least_path))
        st.sidebar.success("least_balanced_stations.csv cargado")
    else:
        st.sidebar.warning("No se encontró data/least_balanced_stations.csv (opcional)")

    if static_path.exists():
        st.session_state["static_stations"] = load_static_stations_from_path(str(static_path))
        st.sidebar.success("static_stations.csv cargado")
    else:
        st.sidebar.info("No se encontró data/static_stations.csv (opcional)")

    if trips_path.exists():
        st.session_state["trips"] = load_trips_from_path(str(trips_path))
        st.sidebar.success("eco_bici_trips.csv cargado")
    elif trips_s_path.exists():
        st.session_state["trips"] = load_trips_from_path(str(trips_s_path))
        st.sidebar.success("eco_bici_trips_s.csv cargado")
    else:
        st.sidebar.info("No se encontró eco_bici_trips*.csv (opcional)")

else:
    st.sidebar.caption("No puedes subir archivos.")

# -----------------------------
# Dataset summary
# -----------------------------

st.header("2) Resumen del dataset")

if not _has("station_data"):
    st.info("Carga `station_data.csv` para habilitar el dashboard.")
    st.stop()

station_data = st.session_state["station_data"]

kpis = kpi_basic_health(station_data)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Registros", f"{kpis.get('num_rows', 0):,}")
c2.metric("Estaciones", f"{kpis.get('num_stations', 0):,}")

installed_rate = kpis.get("installed_rate", None)
renting_rate = kpis.get("renting_rate", None)

c3.metric("% estaciones instaladas", f"{installed_rate*100:.1f}%" if installed_rate is not None else "n/a")
c4.metric("% renta", f"{renting_rate*100:.1f}%" if renting_rate is not None else "n/a")

st.caption(
    f"Rango temporal: {kpis.get('date_min')} → {kpis.get('date_max')}"
)

