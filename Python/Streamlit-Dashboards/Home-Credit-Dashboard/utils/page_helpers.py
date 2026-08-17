from pathlib import Path
import pandas as pd
import streamlit as st

from .data_loader import load_data
from .filters import sidebar_filters, apply_filters


def load_home_credit_data() -> pd.DataFrame:
    csv_path = Path(__file__).resolve().parents[1] / "data" / "application_train.csv"
    return load_data(csv_path)


def get_filtered_data() -> pd.DataFrame:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    return apply_filters(df, filters)


def display_metrics(metrics: dict):
    cols = st.columns(4)
    cols[0].metric("Total Applicants", f"{metrics['total_applicants']:,}")
    cols[1].metric("Default Rate", f"{metrics['default_rate']:.2f}%")
    cols[2].metric("Avg Income", f"${metrics['avg_income']:,.0f}")
    cols[3].metric("Avg Credit", f"${metrics['avg_credit']:,.0f}")
    cols2 = st.columns(3)
    cols2[0].metric("Avg Annuity", f"${metrics['avg_annuity']:,.0f}")
    cols2[1].metric("Avg Age", f"{metrics['avg_age']:.1f} yrs")
    cols2[2].metric("Avg Credit/Income", f"{metrics['avg_credit_income_ratio']:.2f}")


def empty_state():
    st.warning("No applicants match the selected filters. Adjust the filters and try again.")
