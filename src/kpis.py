from __future__ import annotations

import pandas as pd


def kpi_basic_health(station_data: pd.DataFrame) -> dict:
    """Basic dataset-level KPIs."""
    n = len(station_data)
    if n == 0:
        return {}

    out = {}
    if "is_installed" in station_data.columns:
        out["installed_rate"] = float(station_data["is_installed"].mean())
    if "is_renting" in station_data.columns:
        out["renting_rate"] = float(station_data["is_renting"].mean())
    if "is_returning" in station_data.columns:
        out["returning_rate"] = float(station_data["is_returning"].mean())

    out["num_rows"] = int(n)
    out["num_stations"] = int(station_data["station_id"].nunique()) if "station_id" in station_data.columns else None
    out["date_min"] = station_data["timestamp"].min()
    out["date_max"] = station_data["timestamp"].max()

    return out


def hourly_availability(station_data: pd.DataFrame) -> pd.DataFrame:
    cols = ["num_bikes_available", "num_docks_available"]
    df = station_data
    if "is_installed" in df.columns:
        df = df[df["is_installed"]]

    out = (df.groupby("hour")[cols].mean().reset_index())
    return out


def distribution_availability(station_data: pd.DataFrame) -> pd.DataFrame:
    """Long format for boxplots."""
    cols = ["num_bikes_available", "num_docks_available"]
    df = station_data[cols].melt(var_name="Type", value_name="Count")
    return df


def top_disabled_stations(station_data: pd.DataFrame, start_hour: int = 5, end_hour: int = 23, top_n: int = 10) -> pd.DataFrame:
    """Sum disabled bikes per station, excluding early hours by default."""
    df = station_data
    if "hour" in df.columns:
        df = df[df["hour"].between(start_hour, end_hour)]
    out = (
        df.groupby("station_id")["num_bikes_disabled"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    return out


def disabled_by_day_of_week(station_data: pd.DataFrame) -> pd.DataFrame:
    out = (
        station_data.groupby("day_of_week", observed=True)["num_bikes_disabled"]
        .sum()
        .reset_index()
    )
    return out


def balance_by_day_of_week(station_data: pd.DataFrame) -> pd.DataFrame:
    out = (
        station_data.groupby("day_of_week", observed=True)["balance_ratio"]
        .mean()
        .reset_index()
    )
    return out


def corr_matrix(station_data: pd.DataFrame) -> pd.DataFrame:
    metrics = ["num_bikes_available", "num_bikes_disabled", "num_docks_available", "num_docks_disabled"]
    return station_data[metrics].corr()


def station_service_levels(station_data: pd.DataFrame) -> pd.DataFrame:
    """Service level per station: % of observations with >=1 bike, >=1 dock, both."""
    df = station_data
    if "is_installed" in df.columns:
        df = df[df["is_installed"]]

    g = df.groupby("station_id")

    out = pd.DataFrame({
        "pct_has_bike": g["num_bikes_available"].apply(lambda s: (s >= 1).mean()),
        "pct_has_dock": g["num_docks_available"].apply(lambda s: (s >= 1).mean()),
        "pct_has_both": g.apply(lambda x: ((x["num_bikes_available"] >= 1) & (x["num_docks_available"] >= 1)).mean()),
        "avg_bikes": g["num_bikes_available"].mean(),
        "avg_docks": g["num_docks_available"].mean(),
        "avg_balance_ratio": g["balance_ratio"].mean(),
        "total_disabled_sum": g["num_bikes_disabled"].sum(),
    }).reset_index()

    return out
