from __future__ import annotations

import io
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st

DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _coerce_bool01(s: pd.Series) -> pd.Series:
    """Convert 0/1, True/False, '0'/'1' to bool safely."""
    if s.dtype == bool:
        return s
    # Common cases: int, float, object with '0'/'1'
    try:
        return s.astype(int).astype(bool)
    except Exception:
        return s.astype(str).str.lower().isin(["true", "1", "yes", "y"])


def _preprocess_station_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "last_reported" in df.columns:
        if np.issubdtype(df["last_reported"].dtype, np.number):
            # Many GBFS feeds store last_reported as UNIX seconds.
            df["last_reported"] = pd.to_datetime(df["last_reported"], unit="s", errors="coerce")
        else:
            df["last_reported"] = pd.to_datetime(df["last_reported"], errors="coerce")

    # Booleans
    for c in ["is_installed", "is_renting", "is_returning", "is_charging"]:
        if c in df.columns:
            df[c] = _coerce_bool01(df[c])

    # Time features
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = pd.Categorical(df["timestamp"].dt.day_name(), categories=DOW_ORDER, ordered=True)
    df["date"] = df["timestamp"].dt.date

    # Balance ratio: bikes / (bikes + docks)
    if {"num_bikes_available", "num_docks_available"}.issubset(df.columns):
        denom = (df["num_bikes_available"] + df["num_docks_available"]).replace({0: np.nan})
        df["balance_ratio"] = df["num_bikes_available"] / denom

    return df


@st.cache_data(show_spinner=False)
def load_station_data_from_path(path: str) -> pd.DataFrame:
    """Load station_data.csv from disk and preprocess."""
    dtypes = {
        "station_id": "int32",
        "num_bikes_available": "int16",
        "num_bikes_disabled": "int16",
        "num_docks_available": "int16",
        "num_docks_disabled": "int16",
        # booleans are handled after load
    }
    df = pd.read_csv(path, dtype=dtypes)
    return _preprocess_station_data(df)


@st.cache_data(show_spinner=False)
def load_station_data_from_bytes(b: bytes) -> pd.DataFrame:
    """Load station_data.csv from bytes (e.g., st.file_uploader) and preprocess."""
    dtypes = {
        "station_id": "int32",
        "num_bikes_available": "int16",
        "num_bikes_disabled": "int16",
        "num_docks_available": "int16",
        "num_docks_disabled": "int16",
    }
    df = pd.read_csv(io.BytesIO(b), dtype=dtypes)
    return _preprocess_station_data(df)


@st.cache_data(show_spinner=False)
def load_least_balanced_from_path(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_least_balanced_from_bytes(b: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(b))


@st.cache_data(show_spinner=False)
def load_static_stations_from_path(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_static_stations_from_bytes(b: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(b))


@st.cache_data(show_spinner=False)
def load_trips_from_path(path: str) -> pd.DataFrame:
    # Keep it flexible: column names may include accents/spaces.
    df = pd.read_csv(path)
    return df


@st.cache_data(show_spinner=False)
def load_trips_from_bytes(b: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(b))
    return df
