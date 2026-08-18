import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis
from utils.charts import line_chart, bar_chart, histogram

st.set_page_config(page_title="Order Analysis")

st.title("Order Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Calculate order-level metrics
        order_summary = df_filtered.groupby("Order ID").agg({
            "Sales": "sum",
            "Profit": "sum",
            "Quantity": "sum",
            "Order Date": "first",
            "Customer Name": "first",
        }).reset_index()
        
        metrics = calc_kpis(df_filtered)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Orders", f"{metrics['total_orders']:,}")
        col2.metric("Avg Order Value", f"${metrics['avg_order_value']:,.0f}")
        col3.metric("Avg Quantity/Order", f"{metrics['total_quantity']/metrics['total_orders']:.1f}")
        col4.metric("Avg Profit/Order", f"${metrics['total_profit']/metrics['total_orders']:,.0f}")
        
        # Orders trend
        st.plotly_chart(line_chart(df_filtered, "Order Date", "Sales", "Orders by Month", freq="ME"), use_container_width=True)
        
        # Orders by Region and Category
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(bar_chart(df_filtered, "Region", "Order ID", "Orders by Region", aggfunc="nunique"), use_container_width=True)
        with col2:
            st.plotly_chart(bar_chart(df_filtered, "Category", "Order ID", "Orders by Category", aggfunc="nunique"), use_container_width=True)
        
        # Orders by Segment
        st.plotly_chart(bar_chart(df_filtered, "Segment", "Order ID", "Orders by Segment", aggfunc="nunique"), use_container_width=True)
        
        # Order Value Distribution
        st.plotly_chart(histogram(order_summary, "Sales", "Order Value Distribution"), use_container_width=True)
        
        # Order Details Table
        st.subheader("Order Details")
        st.dataframe(
            order_summary.rename(columns={"Customer Name": "Customer", "Sales": "Total Sales"})[
                ["Order ID", "Order Date", "Customer", "Total Sales", "Profit", "Quantity"]
            ].sort_values("Order Date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
