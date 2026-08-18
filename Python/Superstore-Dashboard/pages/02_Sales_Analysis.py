import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis
from utils.charts import line_chart, bar_chart, histogram

st.set_page_config(page_title="Sales Analysis")

st.title("Sales Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        metrics = calc_kpis(df_filtered)
        cols = st.columns(5)
        cols[0].metric("Total Sales", f"${metrics['total_sales']:,.0f}")
        cols[1].metric("Avg Sales per Order", f"${metrics['avg_order_value']:,.0f}")
        cols[2].metric("Max Order Sales", f"${df_filtered.groupby('Order ID')['Sales'].sum().max():,.0f}")
        cols[3].metric("Min Order Sales", f"${df_filtered.groupby('Order ID')['Sales'].sum().min():,.0f}")
        cols[4].metric("Orders", f"{metrics['total_orders']:,}")

        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", "Sales by Month", freq="ME"), use_container_width=True)
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", "Sales by Quarter", freq="QE"), use_container_width=True)
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", "Sales by Year", freq="YE"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Region", "Sales", "Sales by Region"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Sales", "Sales by Category"), use_container_width=True)
        st.plotly_chart(histogram(df_filtered, "Sales", "Sales Distribution"), use_container_width=True)
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")