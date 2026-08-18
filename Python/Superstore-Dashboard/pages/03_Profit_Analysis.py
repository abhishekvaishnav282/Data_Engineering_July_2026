import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis
from utils.charts import line_chart, bar_chart, histogram, scatter_chart

st.set_page_config(page_title="Profit Analysis")

st.title("Profit Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        profit_margin = df_filtered['Profit'].sum() / df_filtered['Sales'].sum() * 100 if df_filtered['Sales'].sum() else 0
        cols = st.columns(5)
        cols[0].metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")
        cols[1].metric("Avg Profit", f"${df_filtered['Profit'].mean():,.0f}")
        cols[2].metric("Profit Margin %", f"{profit_margin:.2f}%")
        cols[3].metric("Max Profit", f"${df_filtered['Profit'].max():,.0f}")
        cols[4].metric("Total Loss", f"${df_filtered[df_filtered['Profit'] < 0]['Profit'].sum():,.0f}")

        st.plotly_chart(line_chart(df_filtered, "Order Date", "Profit", "Monthly Profit Trend", freq="ME"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Region", "Profit", "Profit by Region"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Profit", "Profit by Category"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Sub-Category", "Profit", "Profit by Sub-Category", top_n=20), use_container_width=True)
        st.plotly_chart(histogram(df_filtered, "Profit", "Profit Distribution"), use_container_width=True)
        st.plotly_chart(scatter_chart(df_filtered, "Sales", "Profit", "Region", "Sales vs Profit"), use_container_width=True)

        st.markdown("**Important Insights**")
        st.write({
            "Most Profitable Category": df_filtered.groupby('Category')['Profit'].sum().idxmax(),
            "Most Profitable Region": df_filtered.groupby('Region')['Profit'].sum().idxmax(),
            "Highest Loss Category": df_filtered.groupby('Category')['Profit'].sum().idxmin(),
            "Highest Loss Product": df_filtered.groupby('Product Name')['Profit'].sum().idxmin(),
        })
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")