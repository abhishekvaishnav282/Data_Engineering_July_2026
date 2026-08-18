import streamlit as st
from utils.page_helpers import load_superstore_data
from utils.filters import sidebar_filters, apply_filters
from utils.charts import bar_chart

st.set_page_config(page_title="State Analysis")

st.title("State Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    state_filter = st.sidebar.multiselect("State", options=sorted(df['State'].dropna().unique()), default=sorted(df['State'].dropna().unique()))
    df_filtered = apply_filters(df, filters)
    df_filtered = df_filtered[df_filtered['State'].isin(state_filter)]
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        state_summary = df_filtered.groupby('State').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum'), Orders=('Order ID', 'nunique'), Customers=('Customer ID', 'nunique')).reset_index()
        st.dataframe(state_summary)

        st.plotly_chart(bar_chart(df_filtered, 'State', 'Sales', 'Top 10 States by Sales', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'State', 'Profit', 'Top 10 States by Profit', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered[df_filtered['Profit'] < 0], 'State', 'Profit', 'Bottom 10 States by Profit', top_n=10), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'State', 'Order ID', 'Orders by State'), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, 'State', 'Sales', 'Sales and Profit by State'), use_container_width=True)
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")