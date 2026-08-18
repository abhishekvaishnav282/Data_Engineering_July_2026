import streamlit as st
from utils.page_helpers import load_superstore_data, display_metrics
from utils.kpis import calc_kpis, top_bottom_summary
from utils.charts import line_chart, bar_chart, scatter_chart

st.set_page_config(
    page_title="Superstore Sales Analytics",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("🏪 Superstore Sales Analytics Dashboard")
st.markdown(
    """
    Welcome to the comprehensive **Superstore Sales Analytics Dashboard** with **20 detailed analysis pages**.
    
    Use the sidebar navigation to explore different aspects of your sales data:
    - **Executive & Overview Pages**: Overall business performance snapshots
    - **Dimensional Analysis**: Deep dives into regions, states, cities, categories, and products
    - **Customer & Segment Analysis**: Understand customer behavior and segmentation
    - **Financial Analysis**: Profit, loss, discount, and growth metrics
    - **Time Series & Trends**: Temporal patterns and year-over-year growth
    - **Data Explorer**: Raw data exploration with custom filters and downloads
    """
)

with st.expander("📋 Dashboard Overview"):
    st.write("""
    **20 Pages Available:**
    
    1. **Executive Overview** - High-level business KPIs and trends
    2. **Sales Analysis** - Sales by time periods, regions, and categories
    3. **Profit Analysis** - Profitability metrics and insights
    4. **Regional Analysis** - Performance comparison across regions
    5. **State Analysis** - State-level sales and profit analysis
    6. **City Analysis** - City-level performance metrics
    7. **Category Analysis** - Product category breakdown
    8. **Sub-Category Analysis** - Detailed sub-category performance
    9. **Product Analysis** - Individual product performance
    10. **Customer Analysis** - Customer contribution and behavior
    11. **Customer Segment Analysis** - Consumer, Corporate, Home Office segments
    12. **Order Analysis** - Order-level metrics and trends
    13. **Shipping Analysis** - Ship mode efficiency and distribution
    14. **Discount Analysis** - Impact of discounts on sales and profit
    15. **Loss Analysis** - Identification of loss-making orders and products
    16. **Time Series Analysis** - Trends at various time granularities
    17. **Growth Analysis** - Month-over-month, quarter-over-quarter, year-over-year growth
    18. **Sales vs Profit Analysis** - Relationship between revenue and profitability
    19. **Top & Bottom Performers** - Quick view of best and worst performers
    20. **Data Explorer** - Interactive data exploration with export options
    """)

with st.expander("📊 Dataset and Instructions"):
    st.write(
        """
        **To use this dashboard:**
        1. Place your Excel file at: `superstore_dashboard/data/Sample_Superstore_updated.xlsx`
        2. Use the sidebar filters available on all pages to refine your analysis
        3. Navigate between pages using the Streamlit page menu on the left
        
        **Expected columns in your dataset:**
        Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, 
        Segment, Country, City, State, Postal Code, Region, Product ID, Category, 
        Sub-Category, Product Name, Sales, Quantity, Discount, Profit
        """
    )

if st.button("🔄 Reload Data"):
    st.rerun()

st.header("Executive Summary")

try:
    df = load_superstore_data()
    metrics = calc_kpis(df)
    display_metrics(df, metrics)

    st.subheader("📈 Key Snapshot")
    summary = top_bottom_summary(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.info(f"🏆 Best Region by Sales: **{summary['best_region_sales']}**")
    col2.info(f"📦 Best Category: **{summary['best_category_sales']}**")
    col3.info(f"📅 Highest Sales Month: **{summary['highest_sales_month']}**")
    col4.info(f"💰 Highest Profit Month: **{summary['highest_profit_month']}**")

    st.divider()

    # Quick charts
    st.subheader("Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(line_chart(df, "Order Date", "Sales",
                        "Monthly Sales Trend"), use_container_width=True)
    with col2:
        st.plotly_chart(bar_chart(df, "Region", "Sales",
                        "Sales by Region"), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(df, "Category", "Sales",
                        "Sales by Category"), use_container_width=True)
    with col2:
        st.plotly_chart(scatter_chart(df, "Sales", "Profit",
                        "Region", "Sales vs Profit"), use_container_width=True)

except FileNotFoundError:
    st.error("❌ Sample_Superstore_updated.xlsx not found in superstore_dashboard/data/")
    st.info("Please add your dataset file and refresh the page.")
