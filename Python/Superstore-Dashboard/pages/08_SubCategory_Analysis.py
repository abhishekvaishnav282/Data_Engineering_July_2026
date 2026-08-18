import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_subcategory_kpis
from utils.charts import bar_chart, horizontal_bar_chart

st.set_page_config(page_title="Sub-Category Analysis")

st.title("Sub-Category Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        st.subheader("Sub-Category Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sub-Categories", df_filtered["Sub-Category"].nunique())
        col2.metric("Best Sub-Category", df_filtered.groupby("Sub-Category")["Sales"].sum().idxmax())
        col3.metric("Most Profitable", df_filtered.groupby("Sub-Category")["Profit"].sum().idxmax())
        
        # Top 10 by Sales
        st.plotly_chart(
            bar_chart(df_filtered, "Sub-Category", "Sales", "Top 10 Sub-Categories by Sales", top_n=10),
            use_container_width=True
        )
        
        # Top 10 by Profit
        st.plotly_chart(
            bar_chart(df_filtered, "Sub-Category", "Profit", "Top 10 Sub-Categories by Profit", top_n=10),
            use_container_width=True
        )
        
        # Bottom 10 by Profit
        bottom_profit = df_filtered.groupby("Sub-Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(10)
        st.plotly_chart(
            horizontal_bar_chart(bottom_profit, "Sub-Category", "Profit", "Bottom 10 Sub-Categories by Profit"),
            use_container_width=True
        )
        
        # Full Sub-Category Table
        st.subheader("Sub-Category Summary")
        subcategory_kpis = get_subcategory_kpis(df_filtered)
        st.dataframe(
            subcategory_kpis[["Sub-Category", "Sales", "Profit", "Quantity", "Avg Discount", "Profit Margin %"]],
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
