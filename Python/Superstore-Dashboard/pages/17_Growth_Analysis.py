import streamlit as st
import pandas as pd
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_growth_metrics
from utils.charts import line_chart

st.set_page_config(page_title="Growth Analysis")

st.title("Sales Growth Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Get growth metrics
        growth_df = get_growth_metrics(df_filtered)
        
        # Current metrics
        current_month = growth_df.iloc[-1]
        prev_month = growth_df.iloc[-2] if len(growth_df) > 1 else None
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Month Sales", f"${current_month['Sales']:,.0f}")
        col2.metric("Previous Month Sales", f"${prev_month['Sales']:,.0f}" if prev_month is not None else "N/A")
        col3.metric("MoM Growth %", f"{current_month['Sales_Growth_%']:.2f}%" if pd.notna(current_month['Sales_Growth_%']) else "N/A")
        col4.metric("Latest Profit Growth %", f"{current_month['Profit_Growth_%']:.2f}%" if pd.notna(current_month['Profit_Growth_%']) else "N/A")
        
        # Growth Trends
        st.subheader("Month-over-Month Growth")
        growth_clean = growth_df.dropna()
        if not growth_clean.empty:
            st.plotly_chart(line_chart(growth_clean, "YearMonth", "Sales_Growth_%", "Monthly Sales Growth %", freq="ME"), use_container_width=True)
            st.plotly_chart(line_chart(growth_clean, "YearMonth", "Profit_Growth_%", "Monthly Profit Growth %", freq="ME"), use_container_width=True)
        
        # Quarterly Growth
        df_filtered["Quarter"] = df_filtered["Order Date"].dt.to_period("Q")
        quarterly = df_filtered.groupby("Quarter").agg({
            "Sales": "sum",
            "Profit": "sum",
        }).reset_index()
        quarterly["Sales_Growth_%"] = quarterly["Sales"].pct_change() * 100
        quarterly["Profit_Growth_%"] = quarterly["Profit"].pct_change() * 100
        
        st.subheader("Quarter-over-Quarter Growth")
        st.dataframe(
            quarterly.rename(columns={"Sales_Growth_%": "Sales Growth %", "Profit_Growth_%": "Profit Growth %"}),
            use_container_width=True,
            hide_index=True,
        )
        
        # Year-over-Year Growth
        df_filtered["Year"] = df_filtered["Order Date"].dt.year
        yearly = df_filtered.groupby("Year").agg({
            "Sales": "sum",
            "Profit": "sum",
        }).reset_index()
        yearly["Sales_Growth_%"] = yearly["Sales"].pct_change() * 100
        yearly["Profit_Growth_%"] = yearly["Profit"].pct_change() * 100
        
        st.subheader("Year-over-Year Growth")
        st.dataframe(
            yearly.rename(columns={"Sales_Growth_%": "Sales Growth %", "Profit_Growth_%": "Profit Growth %"}),
            use_container_width=True,
            hide_index=True,
        )
        
        # Growth Details Table
        st.subheader("Monthly Growth Details")
        st.dataframe(
            growth_df.rename(columns={
                "YearMonth": "Month",
                "Sales_Growth_%": "Sales Growth %",
                "Profit_Growth_%": "Profit Growth %",
            }),
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
