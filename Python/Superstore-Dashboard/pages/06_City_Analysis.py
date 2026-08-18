import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.charts import bar_chart

st.set_page_config(page_title="City Analysis")

st.title("City Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    city_filter = st.sidebar.multiselect("City", options=sorted(df['City'].dropna().unique()), default=sorted(df['City'].dropna().unique()))
    df_filtered = apply_filters(df, filters)
    df_filtered = df_filtered[df_filtered['City'].isin(city_filter)]
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        top_cities_sales = df_filtered.groupby('City')['Sales'].sum().nlargest(10)
        top_cities_profit = df_filtered.groupby('City')['Profit'].sum().nlargest(10)
        bottom_cities_profit = df_filtered.groupby('City')['Profit'].sum().nsmallest(10)

        st.metric("Number of Cities", df_filtered['City'].nunique())
        st.metric("Top Sales City", top_cities_sales.idxmax())
        st.metric("Top Profit City", top_cities_profit.idxmax())
        st.metric("Lowest Profit City", bottom_cities_profit.idxmin())

        st.plotly_chart(bar_chart(df_filtered, 'City', 'Sales', 'Top 10 Cities by Sales', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'City', 'Profit', 'Top 10 Cities by Profit', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered[df_filtered['Profit'] < 0], 'City', 'Profit', 'Bottom 10 Cities by Profit', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'City', 'Sales', 'Sales by City', top_n=20), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'City', 'Profit', 'Profit by City', top_n=20), use_container_width=True)
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")