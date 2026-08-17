import numpy as np
import pandas as pd
import streamlit as st


@st.cache_resource
def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]

    # Downcast to the smallest safe numeric dtype - this dataset is 307K rows x 122 columns
    # (~341MB as float64/int64), and on memory-constrained machines that matters a lot more
    # than it did for Superstore's ~10K-row file.
    for col in df.select_dtypes(include="int64").columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")
    for col in df.select_dtypes(include="float64").columns:
        df[col] = pd.to_numeric(df[col], downcast="float")

    new_cols = {}

    # DAYS_BIRTH is negative (days before application) -> convert to a positive age in years
    if "DAYS_BIRTH" in df.columns:
        new_cols["AGE_YEARS"] = (-df["DAYS_BIRTH"] / 365).round(1)

    # DAYS_EMPLOYED uses 365243 as a sentinel for "not currently employed" (mostly pensioners) -
    # treat it as missing before converting to years, otherwise it reads as ~1000 years employed
    if "DAYS_EMPLOYED" in df.columns:
        days_employed = df["DAYS_EMPLOYED"].replace(365243, np.nan)
        new_cols["YEARS_EMPLOYED"] = (-days_employed / 365).round(1)

    # Derived affordability ratios
    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        new_cols["CREDIT_INCOME_RATIO"] = (df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]).round(2)
    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        new_cols["ANNUITY_INCOME_RATIO"] = (df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]).round(2)

    # Readable label for the TARGET flag, used for chart legends/labels
    if "TARGET" in df.columns:
        new_cols["RISK_LABEL"] = df["TARGET"].map({0: "Repaid", 1: "Default"})

    df = pd.concat([df, pd.DataFrame(new_cols, index=df.index)], axis=1)

    for col in df.select_dtypes(include="float64").columns:
        df[col] = pd.to_numeric(df[col], downcast="float")

    # The per-column downcast loops above each reassign one column at a time, which leaves
    # the DataFrame's internal block structure fragmented (harmless, but pandas warns loudly
    # the moment any page later adds a column). Since this runs once per cache population
    # (@st.cache_resource), paying for one consolidating copy here is worth it to keep every
    # downstream page warning-free.
    df = df.copy()

    return df
