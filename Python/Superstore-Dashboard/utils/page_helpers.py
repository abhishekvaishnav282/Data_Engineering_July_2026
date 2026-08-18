from pathlib import Path
import pandas as pd
import streamlit as st

from .data_loader import load_data
from .filters import sidebar_filters, apply_filters
from .kpis import calc_kpis


def load_superstore_data() -> pd.DataFrame:
    csv_path = Path(__file__).resolve(
    ).parents[1] / "data" / "Sample_Superstore_updated.xlsx"
    return load_data(csv_path)


def get_filtered_data() -> pd.DataFrame:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    return apply_filters(df, filters)


def display_metrics(df: pd.DataFrame, metrics: dict):
    cols = st.columns(4)
    cols[0].metric("Total Sales", f"${metrics['total_sales']:,.0f}")
    cols[1].metric("Total Profit", f"${metrics['total_profit']:,.0f}")
    cols[2].metric("Orders", f"{metrics['total_orders']:,}")
    cols[3].metric("Customers", f"{metrics['total_customers']:,}")
    cols2 = st.columns(3)
    cols2[0].metric("Quantity", f"{metrics['total_quantity']:,}")
    cols2[1].metric("Margin %", f"{metrics['profit_margin']:.2f}%")
    cols2[2].metric("Avg Order Value", f"${metrics['avg_order_value']:,.0f}")


def empty_state():
    st.warning(
        "No data is available for the selected filters. Adjust the filters and try again.")
