import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, top_bottom_summary
from utils.charts import line_chart, bar_chart, scatter_chart

st.set_page_config(page_title="Executive Overview")

st.title("Executive Overview")

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
        cols[1].metric("Total Profit", f"${metrics['total_profit']:,.0f}")
        cols[2].metric("Total Orders", f"{metrics['total_orders']:,}")
        cols[3].metric("Total Quantity", f"{metrics['total_quantity']:,}")
        cols[4].metric("Profit Margin %", f"{metrics['profit_margin']:.2f}%")

        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", "Monthly Sales Trend"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Region", "Sales", "Sales by Region"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Sales", "Sales by Category"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Profit", "Profit by Category"), use_container_width=True)
        st.plotly_chart(scatter_chart(df_filtered, "Sales", "Profit", "Region", "Sales vs Profit"), use_container_width=True)

        summary = top_bottom_summary(df_filtered)
        st.subheader("Additional Insights")
        st.write(summary)
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
