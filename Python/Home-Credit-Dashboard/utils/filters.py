import streamlit as st
import pandas as pd


def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")

    age_min, age_max = st.sidebar.slider(
        "Age range (years)",
        min_value=int(df["AGE_YEARS"].min()),
        max_value=int(df["AGE_YEARS"].max()),
        value=(int(df["AGE_YEARS"].min()), int(df["AGE_YEARS"].max())),
    )

    gender = st.sidebar.multiselect(
        "Gender",
        options=sorted(df["CODE_GENDER"].dropna().unique()),
        default=sorted(df["CODE_GENDER"].dropna().unique()),
    )
    contract_type = st.sidebar.multiselect(
        "Contract Type",
        options=sorted(df["NAME_CONTRACT_TYPE"].dropna().unique()),
        default=sorted(df["NAME_CONTRACT_TYPE"].dropna().unique()),
    )
    education = st.sidebar.multiselect(
        "Education",
        options=sorted(df["NAME_EDUCATION_TYPE"].dropna().unique()),
        default=sorted(df["NAME_EDUCATION_TYPE"].dropna().unique()),
    )
    family_status = st.sidebar.multiselect(
        "Family Status",
        options=sorted(df["NAME_FAMILY_STATUS"].dropna().unique()),
        default=sorted(df["NAME_FAMILY_STATUS"].dropna().unique()),
    )
    income_type = st.sidebar.multiselect(
        "Income Type",
        options=sorted(df["NAME_INCOME_TYPE"].dropna().unique()),
        default=sorted(df["NAME_INCOME_TYPE"].dropna().unique()),
    )

    filters = {
        "age_min": age_min,
        "age_max": age_max,
        "CODE_GENDER": gender,
        "NAME_CONTRACT_TYPE": contract_type,
        "NAME_EDUCATION_TYPE": education,
        "NAME_FAMILY_STATUS": family_status,
        "NAME_INCOME_TYPE": income_type,
    }
    return filters


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_filtered = df.copy()
    df_filtered = df_filtered[
        (df_filtered["AGE_YEARS"] >= filters["age_min"]) & (df_filtered["AGE_YEARS"] <= filters["age_max"])
    ]
    if filters["CODE_GENDER"]:
        df_filtered = df_filtered[df_filtered["CODE_GENDER"].isin(filters["CODE_GENDER"])]
    if filters["NAME_CONTRACT_TYPE"]:
        df_filtered = df_filtered[df_filtered["NAME_CONTRACT_TYPE"].isin(filters["NAME_CONTRACT_TYPE"])]
    if filters["NAME_EDUCATION_TYPE"]:
        df_filtered = df_filtered[df_filtered["NAME_EDUCATION_TYPE"].isin(filters["NAME_EDUCATION_TYPE"])]
    if filters["NAME_FAMILY_STATUS"]:
        df_filtered = df_filtered[df_filtered["NAME_FAMILY_STATUS"].isin(filters["NAME_FAMILY_STATUS"])]
    if filters["NAME_INCOME_TYPE"]:
        df_filtered = df_filtered[df_filtered["NAME_INCOME_TYPE"].isin(filters["NAME_INCOME_TYPE"])]
    return df_filtered
