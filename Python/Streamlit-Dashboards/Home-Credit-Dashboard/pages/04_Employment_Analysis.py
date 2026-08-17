import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_segment_summary
from utils.charts import bar_chart, horizontal_bar_chart, histogram

st.set_page_config(page_title="Employment Analysis")

st.title("Employment Analysis")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        cols = st.columns(5)
        cols[0].metric("Total Applicants", f"{metrics['total_applicants']:,}")
        cols[1].metric("Default Rate", f"{metrics['default_rate']:.2f}%")
        cols[2].metric("Avg Years Employed", f"{df_filtered['YEARS_EMPLOYED'].mean():.1f} yrs")
        cols[3].metric("Avg Income", f"${metrics['avg_income']:,.0f}")
        cols[4].metric("Avg Credit", f"${metrics['avg_credit']:,.0f}")

        st.plotly_chart(bar_chart(df_filtered, "NAME_INCOME_TYPE", None, "Applicants by Income Type"))

        income_type_summary = get_segment_summary(df_filtered, "NAME_INCOME_TYPE")
        st.plotly_chart(bar_chart(income_type_summary, "NAME_INCOME_TYPE", "Default_Rate",
                                   "Default Rate % by Income Type", pre_aggregated=True))

        occupation_summary = get_segment_summary(df_filtered, "OCCUPATION_TYPE", top_n=10)
        st.plotly_chart(horizontal_bar_chart(occupation_summary, "OCCUPATION_TYPE", "Applicants",
                                              "Top 10 Occupations by Applicant Count", pre_aggregated=True))

        organization_summary = get_segment_summary(df_filtered, "ORGANIZATION_TYPE", top_n=10)
        st.plotly_chart(horizontal_bar_chart(organization_summary, "ORGANIZATION_TYPE", "Applicants",
                                              "Top 10 Organization Types by Applicant Count", pre_aggregated=True))

        occupation_risk = get_segment_summary(df_filtered, "OCCUPATION_TYPE").sort_values(
            "Default_Rate", ascending=False).head(10)
        st.plotly_chart(horizontal_bar_chart(occupation_risk, "OCCUPATION_TYPE", "Default_Rate",
                                              "Top 10 Highest-Risk Occupations", pre_aggregated=True))

        st.plotly_chart(histogram(df_filtered, "YEARS_EMPLOYED", "Years Employed Distribution by Risk", color_col="RISK_LABEL"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
