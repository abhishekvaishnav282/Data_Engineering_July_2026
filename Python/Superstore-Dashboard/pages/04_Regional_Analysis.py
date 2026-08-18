import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.charts import bar_chart

st.set_page_config(page_title="Regional Analysis")

st.title("Regional Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        region_sales = df_filtered.groupby('Region')['Sales'].sum()
        region_profit = df_filtered.groupby('Region')['Profit'].sum()
        region_orders = df_filtered.groupby('Region')['Order ID'].nunique()
        region_customers = df_filtered.groupby('Region')['Customer ID'].nunique()
        avg_order_value = df_filtered.groupby('Region').apply(lambda x: x['Sales'].sum() / x['Order ID'].nunique())

        st.dataframe(
            st.session_state.get('region_df') if 'region_df' in st.session_state else None
        )
        st.write("Regional comparison is available via the charts below.")

        st.plotly_chart(bar_chart(df_filtered, 'Region', 'Sales', 'Sales by Region'), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'Region', 'Profit', 'Profit by Region'), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'Region', 'Order ID', 'Orders by Region'), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'Region', 'Quantity', 'Quantity by Region'), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'Region', 'Profit', 'Regional Profit Margin'), use_container_width=True)

        st.data_editor(
            df_filtered.groupby('Region')[['Sales', 'Profit', 'Quantity']].sum().assign(Orders=df_filtered.groupby('Region')['Order ID'].nunique()).assign(Customers=df_filtered.groupby('Region')['Customer ID'].nunique()),
            disabled=True,
        )
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")