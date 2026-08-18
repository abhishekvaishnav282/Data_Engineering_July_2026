import streamlit as st
import pandas as pd
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.charts import line_chart, multi_line_chart

st.set_page_config(page_title="Time Series Analysis")

st.title("Time Series Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Time Granularity Selection
        time_freq = st.radio("Select time granularity:", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"], horizontal=True)
        freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME", "Quarterly": "QE", "Yearly": "YE"}
        freq = freq_map[time_freq]
        
        # Sales Trend
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", f"Sales Trend ({time_freq})", freq=freq), use_container_width=True)
        
        # Profit Trend
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Profit", f"Profit Trend ({time_freq})", freq=freq), use_container_width=True)
        
        # Orders Trend
        order_trend = df_filtered.groupby(pd.Grouper(key="Order Date", freq=freq))["Order ID"].nunique().reset_index()
        order_trend.columns = ["Order Date", "Orders"]
        from utils.charts import bar_chart
        st.plotly_chart(bar_chart(order_trend, "Order Date", "Orders", f"Order Trend ({time_freq})"), use_container_width=True)
        
        # Quantity Trend
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Quantity", f"Quantity Trend ({time_freq})", freq=freq), use_container_width=True)
        
        # Sales vs Profit Comparison
        st.subheader(f"Sales vs Profit Comparison ({time_freq})")
        comparison = df_filtered.groupby(pd.Grouper(key="Order Date", freq=freq))[["Sales", "Profit"]].sum().reset_index()
        st.plotly_chart(
            multi_line_chart(comparison, "Order Date", ["Sales", "Profit"], f"Sales and Profit Comparison", freq="ME"),
            use_container_width=True
        )
        
        # KPI Summary
        st.subheader("Time Period KPIs")
        summary = df_filtered.groupby(pd.Grouper(key="Order Date", freq=freq)).agg({
            "Sales": "sum",
            "Profit": "sum",
            "Quantity": "sum",
            "Order ID": "nunique",
        }).rename(columns={"Order ID": "Orders"}).reset_index()
        summary.columns = ["Period", "Sales", "Profit", "Quantity", "Orders"]
        st.dataframe(summary, use_container_width=True, hide_index=True)
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")

