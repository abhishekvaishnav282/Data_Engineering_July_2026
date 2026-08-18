import streamlit as st
import pandas as pd


def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")
    start_date, end_date = st.sidebar.date_input(
        "Date range",
        value=(df["Order Date"].min(), df["Order Date"].max()),
        min_value=df["Order Date"].min(),
        max_value=df["Order Date"].max(),
    )

    region = st.sidebar.multiselect(
        "Region",
        options=sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique()),
    )
    category = st.sidebar.multiselect(
        "Category",
        options=sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique()),
    )
    segment = st.sidebar.multiselect(
        "Segment",
        options=sorted(df["Segment"].dropna().unique()),
        default=sorted(df["Segment"].dropna().unique()),
    )

    sub_category = st.sidebar.multiselect(
        "Sub-Category",
        options=sorted(df["Sub-Category"].dropna().unique()),
        default=sorted(df["Sub-Category"].dropna().unique()),
    )
    ship_mode = st.sidebar.multiselect(
        "Ship Mode",
        options=sorted(df["Ship Mode"].dropna().unique()),
        default=sorted(df["Ship Mode"].dropna().unique()),
    )

    filters = {
        "start_date": pd.to_datetime(start_date),
        "end_date": pd.to_datetime(end_date),
        "Region": region,
        "Category": category,
        "Segment": segment,
        "Sub-Category": sub_category,
        "Ship Mode": ship_mode,
    }
    return filters


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_filtered = df.copy()
    df_filtered = df_filtered[(df_filtered["Order Date"] >= filters["start_date"]) & (df_filtered["Order Date"] <= filters["end_date"])]
    if filters["Region"]:
        df_filtered = df_filtered[df_filtered["Region"].isin(filters["Region"])]
    if filters["Category"]:
        df_filtered = df_filtered[df_filtered["Category"].isin(filters["Category"])]
    if filters["Segment"]:
        df_filtered = df_filtered[df_filtered["Segment"].isin(filters["Segment"])]
    if filters["Sub-Category"]:
        df_filtered = df_filtered[df_filtered["Sub-Category"].isin(filters["Sub-Category"])]
    if filters["Ship Mode"]:
        df_filtered = df_filtered[df_filtered["Ship Mode"].isin(filters["Ship Mode"])]
    return df_filtered
