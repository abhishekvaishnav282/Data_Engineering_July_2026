import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import get_segment_kpis
from utils.charts import bar_chart, pie_chart

st.set_page_config(page_title="Customer Segment Analysis")

st.title("Customer Segment Analysis")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        st.subheader("Segment Performance")
        
        # KPIs by Segment
        segment_kpis = get_segment_kpis(df_filtered)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Consumer Sales", f"${segment_kpis[segment_kpis['Segment'] == 'Consumer']['Sales'].values[0]:,.0f}" if "Consumer" in segment_kpis["Segment"].values else "$0")
        col2.metric("Corporate Sales", f"${segment_kpis[segment_kpis['Segment'] == 'Corporate']['Sales'].values[0]:,.0f}" if "Corporate" in segment_kpis["Segment"].values else "$0")
        col3.metric("Home Office Sales", f"${segment_kpis[segment_kpis['Segment'] == 'Home Office']['Sales'].values[0]:,.0f}" if "Home Office" in segment_kpis["Segment"].values else "$0")
        
        # Charts
        st.plotly_chart(bar_chart(df_filtered, "Segment", "Sales", "Sales by Segment"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Segment", "Profit", "Profit by Segment"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Segment", "Quantity", "Quantity by Segment"), use_container_width=True)
        st.plotly_chart(bar_chart(df_filtered, "Segment", "Order ID", "Orders by Segment", aggfunc="nunique"), use_container_width=True)
        st.plotly_chart(pie_chart(df_filtered, "Sales", "Segment", "Sales Distribution by Segment"), use_container_width=True)
        
        # Segment Summary Table
        st.subheader("Segment Summary")
        display_cols = ["Segment", "Sales", "Profit", "Quantity", "Orders", "Customers", "Avg Discount", "Profit Margin %"]
        st.dataframe(
            segment_kpis[display_cols].rename(columns={"Profit Margin %": "Margin %"}),
            use_container_width=True,
            hide_index=True,
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
