from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def fig_hourly_availability(df_hourly: pd.DataFrame):
    fig = px.line(
        df_hourly,
        x="hour",
        y=["num_bikes_available", "num_docks_available"],
        markers=True,
        labels={"value": "Average availability", "hour": "Hour"},
    )
    fig.update_layout(title="Overall Bike and Dock Availability by Hour", legend_title_text="")
    fig.update_xaxes(dtick=2)
    return fig


def fig_box_availability(df_long: pd.DataFrame):
    fig = px.box(
        df_long,
        x="Type",
        y="Count",
        points="outliers",
        title="Distribution of Available Bikes and Docks by Station",
    )
    fig.update_layout(xaxis_title="", yaxis_title="Count")
    return fig


def fig_top_disabled(df_top: pd.DataFrame):
    fig = px.bar(
        df_top.sort_values("num_bikes_disabled", ascending=True),
        x="num_bikes_disabled",
        y="station_id",
        orientation="h",
        title="Top Stations with Most Disabled Bikes (Excluding 00:00 to 05:00 AM)",
        labels={"num_bikes_disabled": "Total disabled bikes", "station_id": "Station"},
    )
    return fig


def fig_disabled_by_dow(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="day_of_week",
        y="num_bikes_disabled",
        title="Frequency of Disabled Bikes by Day of the Week",
        labels={"day_of_week": "Day of week", "num_bikes_disabled": "Total disabled bikes"},
    )
    return fig


def fig_balance_by_dow(df: pd.DataFrame):
    fig = px.line(
        df,
        x="day_of_week",
        y="balance_ratio",
        markers=True,
        title="Balance Ratio by Day of the Week",
        labels={"day_of_week": "Day of week", "balance_ratio": "Balance ratio"},
    )
    fig.update_yaxes(range=[0, 1])
    return fig


def fig_corr_matrix(corr: pd.DataFrame):
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix of Station Availability Metrics",
    )
    return fig


def fig_map_least_balanced(df: pd.DataFrame):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="balance_ratio",
        hover_name="name",
        hover_data={"station_id": True, "capacity": True, "balance_ratio": ":.3f"},
        zoom=10,
        height=520,
        mapbox_style="carto-positron",
        title="Geospatial Distribution of Least Balanced Stations",
    )
    return fig