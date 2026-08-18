import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_customer_kpis, calc_kpis
from utils.charts import bar_chart, horizontal_bar_chart, histogram

st.set_page_config(page_title="Customer Analysis")

st.title("Customer Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Customers", metrics["total_customers"])
        col2.metric("Avg Sales per Customer", f"${metrics['total_sales']/metrics['total_customers']:,.0f}")
        col3.metric("Avg Profit per Customer", f"${metrics['total_profit']/metrics['total_customers']:,.0f}")
        col4.metric("Top Customer", df_filtered.groupby("Customer Name")["Sales"].sum().idxmax()[:20])
        
        # Top Customers by Sales
        st.plotly_chart(
            bar_chart(df_filtered, "Customer Name", "Sales", "Top 10 Customers by Sales", top_n=10),
            use_container_width=True
        )
        
        # Top Customers by Profit
        st.plotly_chart(
            bar_chart(df_filtered, "Customer Name", "Profit", "Top 10 Customers by Profit", top_n=10),
            use_container_width=True
        )
        
        # Customer Order Frequency
        order_freq = df_filtered.groupby("Customer Name")["Order ID"].nunique().reset_index()
        order_freq.columns = ["Customer Name", "Orders"]
        order_freq = order_freq.sort_values("Orders", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(order_freq, "Customer Name", "Orders", "Top 15 Customers by Order Frequency"),
            use_container_width=True
        )
        
        # Customer Table
        st.subheader("Customer Summary")
        customer_kpis = get_customer_kpis(df_filtered)
        st.dataframe(
            customer_kpis[["Customer Name", "Segment", "Orders", "Sales", "Profit", "Quantity"]],
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
