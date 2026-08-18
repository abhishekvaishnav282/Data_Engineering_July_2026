import streamlit as st
import pandas as pd
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis

st.set_page_config(page_title="Data Explorer")

st.title("Detailed Data Explorer")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Additional filters for this page
        st.subheader("Additional Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_states = st.multiselect(
                "Filter by State",
                options=sorted(df_filtered["State"].unique()),
                default=list(df_filtered["State"].unique()),
            )
        
        with col2:
            selected_cities = st.multiselect(
                "Filter by City",
                options=sorted(df_filtered[df_filtered["State"].isin(selected_states)]["City"].unique()),
                default=list(df_filtered[df_filtered["State"].isin(selected_states)]["City"].unique()),
            )
        
        with col3:
            selected_shipmode = st.multiselect(
                "Filter by Ship Mode",
                options=sorted(df_filtered["Ship Mode"].unique()),
                default=list(df_filtered["Ship Mode"].unique()),
            )
        
        # Apply additional filters
        df_explorer = df_filtered[
            (df_filtered["State"].isin(selected_states)) &
            (df_filtered["City"].isin(selected_cities)) &
            (df_filtered["Ship Mode"].isin(selected_shipmode))
        ]
        
        # Search functionality
        st.subheader("Search")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_order = st.text_input("Search by Order ID")
            if search_order:
                df_explorer = df_explorer[df_explorer["Order ID"].astype(str).str.contains(search_order, na=False)]
        
        with col2:
            search_customer = st.text_input("Search by Customer Name")
            if search_customer:
                df_explorer = df_explorer[df_explorer["Customer Name"].str.contains(search_customer, case=False, na=False)]
        
        with col3:
            search_product = st.text_input("Search by Product Name")
            if search_product:
                df_explorer = df_explorer[df_explorer["Product Name"].str.contains(search_product, case=False, na=False)]
        
        # Summary Metrics
        st.subheader("Summary Metrics")
        metrics = calc_kpis(df_explorer)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Number of Records", len(df_explorer))
        col2.metric("Total Sales", f"${metrics['total_sales']:,.0f}")
        col3.metric("Total Profit", f"${metrics['total_profit']:,.0f}")
        col4.metric("Total Quantity", f"{metrics['total_quantity']:,.0f}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Discount", f"{df_explorer['Discount'].mean()*100:.2f}%")
        col2.metric("Profit Margin %", f"{metrics['profit_margin']:.2f}%")
        col3.metric("Avg Order Value", f"${metrics['avg_order_value']:,.0f}")
        
        # Data Table
        st.subheader("Filtered Data")
        st.dataframe(
            df_explorer[[
                "Order ID", "Order Date", "Ship Date", "Ship Mode",
                "Customer Name", "Segment", "City", "State",
                "Product Name", "Category", "Sub-Category",
                "Sales", "Quantity", "Discount", "Profit"
            ]].sort_values("Order Date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        
        # Download Options
        st.subheader("Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            # Download filtered data as CSV
            csv = df_explorer.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name="superstore_filtered.csv",
                mime="text/csv",
            )
        
        with col2:
            # Download summary CSV
            summary_df = pd.DataFrame({
                "Metric": ["Number of Records", "Total Sales", "Total Profit", "Total Quantity", "Avg Discount", "Profit Margin %", "Avg Order Value"],
                "Value": [len(df_explorer), metrics['total_sales'], metrics['total_profit'], metrics['total_quantity'], 
                         f"{df_explorer['Discount'].mean()*100:.2f}%", f"{metrics['profit_margin']:.2f}%", metrics['avg_order_value']]
            })
            summary_csv = summary_df.to_csv(index=False)
            st.download_button(
                label="Download Summary as CSV",
                data=summary_csv,
                file_name="superstore_summary.csv",
                mime="text/csv",
            )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
