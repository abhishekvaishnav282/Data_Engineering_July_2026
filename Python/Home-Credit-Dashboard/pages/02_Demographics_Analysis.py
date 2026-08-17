import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_segment_summary
from utils.charts import bar_chart, histogram

st.set_page_config(page_title="Demographics Analysis")

st.title("Demographics Analysis")

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
        cols[2].metric("Avg Age", f"{metrics['avg_age']:.1f} yrs")
        cols[3].metric("Avg Family Members", f"{df_filtered['CNT_FAM_MEMBERS'].mean():.1f}")
        cols[4].metric("Avg Children", f"{df_filtered['CNT_CHILDREN'].mean():.1f}")

        st.plotly_chart(bar_chart(df_filtered, "CODE_GENDER", None, "Applicants by Gender"))

        gender_summary = get_segment_summary(df_filtered, "CODE_GENDER")
        st.plotly_chart(bar_chart(gender_summary, "CODE_GENDER", "Default_Rate",
                                   "Default Rate % by Gender", pre_aggregated=True))

        st.plotly_chart(bar_chart(df_filtered, "NAME_FAMILY_STATUS", None, "Applicants by Family Status"))

        family_summary = get_segment_summary(df_filtered, "NAME_FAMILY_STATUS")
        st.plotly_chart(bar_chart(family_summary, "NAME_FAMILY_STATUS", "Default_Rate",
                                   "Default Rate % by Family Status", pre_aggregated=True))

        st.plotly_chart(bar_chart(df_filtered, "NAME_EDUCATION_TYPE", None, "Applicants by Education"))

        st.plotly_chart(bar_chart(df_filtered, "CNT_CHILDREN", None, "Applicants by Number of Children", top_n=8))

        st.plotly_chart(histogram(df_filtered, "AGE_YEARS", "Age Distribution by Risk", color_col="RISK_LABEL"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
