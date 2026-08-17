import streamlit as st
from utils.page_helpers import load_home_credit_data, display_metrics, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, risk_snapshot, get_segment_summary
from utils.charts import pie_chart, bar_chart, histogram, scatter_chart

st.set_page_config(page_title="Executive Overview")

st.title("Executive Overview")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        display_metrics(metrics)

        st.subheader("📈 Key Snapshot")
        snapshot = risk_snapshot(df_filtered)
        col1, col2, col3, col4 = st.columns(4)
        col1.info(f"⚠️ Highest Risk Education: **{snapshot['highest_risk_education']}**")
        col2.info(f"✅ Lowest Risk Education: **{snapshot['lowest_risk_education']}**")
        col3.info(f"⚠️ Highest Risk Income Type: **{snapshot['highest_risk_income_type']}**")
        col4.info(f"⚠️ Highest Risk Family Status: **{snapshot['highest_risk_family_status']}**")

        st.divider()
        st.subheader("Portfolio Breakdown")

        st.plotly_chart(pie_chart(df_filtered, "RISK_LABEL", "Repaid vs Default"))
        st.plotly_chart(bar_chart(df_filtered, "NAME_CONTRACT_TYPE", None, "Applicants by Contract Type"))

        education_summary = get_segment_summary(df_filtered, "NAME_EDUCATION_TYPE")
        st.plotly_chart(bar_chart(education_summary, "NAME_EDUCATION_TYPE", "Default_Rate",
                                   "Default Rate % by Education", pre_aggregated=True))

        st.plotly_chart(histogram(df_filtered, "AMT_INCOME_TOTAL", "Income Distribution by Risk", color_col="RISK_LABEL"))

        sample_df = df_filtered.sample(n=min(2000, len(df_filtered)), random_state=42)
        st.plotly_chart(scatter_chart(sample_df, "AMT_INCOME_TOTAL", "AMT_CREDIT", "RISK_LABEL",
                                       "Income vs Credit (sampled)"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
