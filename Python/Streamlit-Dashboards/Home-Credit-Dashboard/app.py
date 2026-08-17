import streamlit as st
from utils.page_helpers import load_home_credit_data, display_metrics
from utils.kpis import calc_kpis, risk_snapshot
from utils.charts import bar_chart, pie_chart, histogram, scatter_chart

st.set_page_config(
    page_title="Home Credit Risk Analytics",
    page_icon=":bank:",
    layout="wide",
)

st.title(":bank: Home Credit Risk Analytics Dashboard")
st.markdown(
    """
    Welcome to the **Home Credit Risk Analytics Dashboard** with **10 detailed analysis pages**.

    Use the sidebar navigation to explore different aspects of the loan applicant data:
    - **Executive Overview**: Overall portfolio snapshot and default rate
    - **Demographics & Employment**: Who the applicants are and what they do
    - **Income, Credit & Housing**: Financial profile and living situation
    - **Risk Signals**: External credit scores, default risk by segment, credit bureau history
    - **Correlation Explorer & Data Explorer**: Deeper numeric relationships and raw data access
    """
)

with st.expander("📋 Dashboard Overview"):
    st.write("""
    **10 Pages Available:**

    1. **Executive Overview** - Portfolio-wide KPIs and default rate snapshot
    2. **Demographics Analysis** - Gender, family status, children, age, education
    3. **Income & Credit Analysis** - Income, credit, annuity, goods price, affordability ratios
    4. **Employment Analysis** - Income type, occupation, organization, years employed
    5. **Housing & Region Analysis** - Housing type, car/realty ownership, region rating
    6. **External Source Analysis** - EXT_SOURCE_1/2/3 credit bureau scores vs default risk
    7. **Default Risk Analysis** - Default rate broken down across every major segment
    8. **Credit Bureau & Social Circle** - Bureau enquiry history and social circle defaults
    9. **Correlation Explorer** - Numeric features most correlated with default
    10. **Data Explorer** - Raw filtered data with search and CSV export
    """)

with st.expander("📊 Dataset and Instructions"):
    st.write(
        """
        **To use this dashboard:**
        1. Place `application_train.csv` at: `Home Credit Dashboard/data/application_train.csv`
        2. Use the sidebar filters available on all pages to refine the applicant population
        3. Navigate between pages using the Streamlit page menu on the left

        **Key columns in this dataset:**
        SK_ID_CURR, TARGET, CODE_GENDER, NAME_EDUCATION_TYPE, NAME_FAMILY_STATUS,
        NAME_INCOME_TYPE, NAME_HOUSING_TYPE, AMT_INCOME_TOTAL, AMT_CREDIT, AMT_ANNUITY,
        DAYS_BIRTH, DAYS_EMPLOYED, EXT_SOURCE_1/2/3, and ~110 additional applicant attributes.
        """
    )

if st.button("🔄 Clear Cache & Reload"):
    st.cache_data.clear()
    st.rerun()

st.header("Executive Summary")

try:
    df = load_home_credit_data()
    metrics = calc_kpis(df)
    display_metrics(metrics)

    st.subheader("📈 Key Snapshot")
    snapshot = risk_snapshot(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.info(f"⚠️ Highest Risk Education: **{snapshot['highest_risk_education']}**")
    col2.info(f"✅ Lowest Risk Education: **{snapshot['lowest_risk_education']}**")
    col3.info(f"⚠️ Highest Risk Income Type: **{snapshot['highest_risk_income_type']}**")
    col4.info(f"⚠️ Highest Risk Family Status: **{snapshot['highest_risk_family_status']}**")

    st.divider()

    # Quick charts
    st.subheader("Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(pie_chart(df, "RISK_LABEL", "Repaid vs Default"))
    with col2:
        st.plotly_chart(bar_chart(df, "NAME_EDUCATION_TYPE", None, "Applicants by Education"))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(histogram(df, "AGE_YEARS", "Age Distribution by Risk", color_col="RISK_LABEL"))
    with col2:
        sample_df = df.sample(n=min(2000, len(df)), random_state=42)
        st.plotly_chart(scatter_chart(sample_df, "AMT_INCOME_TOTAL", "AMT_CREDIT", "RISK_LABEL", "Income vs Credit (2,000-row sample)"))

except FileNotFoundError:
    st.error("❌ application_train.csv not found in Home Credit Dashboard/data/")
    st.info("Please add the dataset file and refresh the page.")
