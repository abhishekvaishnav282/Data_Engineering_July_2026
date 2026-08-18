import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.charts import scatter_chart

st.set_page_config(page_title="Sales vs Profit Analysis")

st.title("Sales vs Profit Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Grouping options
        grouping = st.selectbox(
            "Select grouping for visualization:",
            ["Region", "Category", "Segment", "Sub-Category"],
        )
        
        # Main visualization options
        viz_type = st.radio("Select visualization:", ["Sales vs Profit", "Sales vs Discount", "Quantity vs Sales", "Quantity vs Profit", "Discount vs Profit"], horizontal=True)
        
        if viz_type == "Sales vs Profit":
            st.plotly_chart(scatter_chart(df_filtered, "Sales", "Profit", grouping, "Sales vs Profit"), use_container_width=True)
        elif viz_type == "Sales vs Discount":
            st.plotly_chart(scatter_chart(df_filtered, "Sales", "Discount", grouping, "Sales vs Discount"), use_container_width=True)
        elif viz_type == "Quantity vs Sales":
            st.plotly_chart(scatter_chart(df_filtered, "Quantity", "Sales", grouping, "Quantity vs Sales"), use_container_width=True)
        elif viz_type == "Quantity vs Profit":
            st.plotly_chart(scatter_chart(df_filtered, "Quantity", "Profit", grouping, "Quantity vs Profit"), use_container_width=True)
        elif viz_type == "Discount vs Profit":
            st.plotly_chart(scatter_chart(df_filtered, "Discount", "Profit", grouping, "Discount vs Profit"), use_container_width=True)
        
        # Insights
        st.subheader("Key Insights")
        
        # High Sales + High Profit
        high_high = df_filtered[(df_filtered["Sales"] > df_filtered["Sales"].quantile(0.75)) & 
                                (df_filtered["Profit"] > df_filtered["Profit"].quantile(0.75))]
        st.metric("High Sales + High Profit Orders", len(high_high))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # High Sales + Low Profit
            high_low = df_filtered[(df_filtered["Sales"] > df_filtered["Sales"].quantile(0.75)) & 
                                   (df_filtered["Profit"] < df_filtered["Profit"].quantile(0.25))]
            st.metric("High Sales + Low Profit", len(high_low))
        
        with col2:
            # Low Sales + High Profit
            low_high = df_filtered[(df_filtered["Sales"] < df_filtered["Sales"].quantile(0.25)) & 
                                   (df_filtered["Profit"] > df_filtered["Profit"].quantile(0.75))]
            st.metric("Low Sales + High Profit", len(low_high))
        
        with col3:
            # Loss Orders
            loss = df_filtered[df_filtered["Profit"] < 0]
            st.metric("Loss Orders", len(loss))
        
        # Detailed Analysis
        st.subheader("Detailed Breakdown by Region")
        region_analysis = df_filtered.groupby("Region").agg({
            "Sales": ["sum", "mean"],
            "Profit": ["sum", "mean"],
            "Quantity": "mean",
            "Discount": "mean",
        }).round(2)
        st.dataframe(region_analysis, use_container_width=True)
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
