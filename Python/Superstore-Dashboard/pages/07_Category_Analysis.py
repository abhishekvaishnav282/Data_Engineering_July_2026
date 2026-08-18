import streamlit as st
from utils.page_helpers import load_superstore_data, get_filtered_data, display_metrics, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_category_kpis
from utils.charts import bar_chart, pie_chart

st.set_page_config(page_title="Category Analysis")

st.title("Category Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # By Category
        st.subheader("Sales by Category")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Categories", df_filtered["Category"].nunique())
        col2.metric("Top Category", df_filtered.groupby("Category")["Sales"].sum().idxmax())
        col3.metric("Most Profitable", df_filtered.groupby("Category")["Profit"].sum().idxmax())
        
        st.plotly_chart(bar_chart(df_filtered, "Category", "Sales", "Sales by Category"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Profit", "Profit by Category"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Category", "Quantity", "Quantity by Category"), use_container_width=True)
        st.plotly_chart(pie_chart(df_filtered, "Sales", "Category", "Sales Distribution by Category"), use_container_width=True)
        
        # Category KPI Table
        st.subheader("Category Performance Summary")
        category_kpis = get_category_kpis(df_filtered)
        st.dataframe(
            category_kpis[["Category", "Sales", "Profit", "Quantity", "Orders", "Profit Margin %"]].rename(
                columns={"Profit Margin %": "Margin %"}
            ),
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
