import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_product_kpis
from utils.charts import bar_chart, horizontal_bar_chart, scatter_chart

st.set_page_config(page_title="Product Analysis")

st.title("Product Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Products", df_filtered["Product Name"].nunique())
        col2.metric("Highest Seller", df_filtered.groupby("Product Name")["Sales"].sum().idxmax()[:20])
        col3.metric("Most Profitable", df_filtered.groupby("Product Name")["Profit"].sum().idxmax()[:20])
        col4.metric("Highest Loss Product", df_filtered[df_filtered["Profit"] < 0].groupby("Product Name")["Profit"].sum().idxmin()[:20] if (df_filtered["Profit"] < 0).any() else "None")
        
        # Top Products
        st.plotly_chart(
            bar_chart(df_filtered, "Product Name", "Sales", "Top 10 Products by Sales", top_n=10),
            use_container_width=True
        )
        
        st.plotly_chart(
            bar_chart(df_filtered, "Product Name", "Profit", "Top 10 Products by Profit", top_n=10),
            use_container_width=True
        )
        
        # Bottom Products
        bottom_profit = df_filtered.groupby("Product Name")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(10)
        st.plotly_chart(
            horizontal_bar_chart(bottom_profit, "Product Name", "Profit", "Bottom 10 Products by Profit"),
            use_container_width=True
        )
        
        # Product Table
        st.subheader("Product Summary")
        product_kpis = get_product_kpis(df_filtered)
        st.dataframe(
            product_kpis[["Product Name", "Category", "Sub-Category", "Sales", "Profit", "Quantity", "Avg Discount", "Profit Margin %"]],
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
