import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_shipping_kpis
from utils.charts import bar_chart, pie_chart

st.set_page_config(page_title="Shipping Analysis")

st.title("Shipping Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Shipping KPIs
        shipping_kpis = get_shipping_kpis(df_filtered)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Shipments", int(shipping_kpis["Shipments"].sum()))
        col2.metric("Most Used Mode", df_filtered["Ship Mode"].mode()[0] if not df_filtered["Ship Mode"].mode().empty else "N/A")
        col3.metric("Avg Shipping Days", f"{df_filtered['Shipping Days'].mean():.1f}")
        col4.metric("Fastest Mode", shipping_kpis.loc[shipping_kpis["Avg Shipping Days"].idxmin(), "Ship Mode"] if not shipping_kpis.empty else "N/A")
        
        # Charts
        st.plotly_chart(bar_chart(df_filtered, "Ship Mode", "Order ID", "Orders by Ship Mode", aggfunc="nunique"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Ship Mode", "Sales", "Sales by Ship Mode"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Ship Mode", "Profit", "Profit by Ship Mode"), use_container_width=True)
        st.plotly_chart(pie_chart(df_filtered, "Sales", "Ship Mode", "Sales Distribution by Ship Mode"), use_container_width=True)
        
        # Shipping Days Analysis
        st.subheader("Shipping Performance")
        st.dataframe(
            shipping_kpis.rename(columns={"Shipments": "Orders", "Avg Shipping Days": "Avg Days"}),
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
