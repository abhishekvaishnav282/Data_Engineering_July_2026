import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_credit_bureau_kpis, get_social_circle_kpis, get_segment_summary
from utils.charts import bar_chart, histogram

st.set_page_config(page_title="Credit Bureau & Social Circle")

st.title("Credit Bureau & Social Circle")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        # Added together via assign() rather than two separate assignments, to avoid
        # fragmenting this already-large (127-column) DataFrame with repeated single-column inserts.
        df_filtered = df_filtered.assign(
            Has_Bureau_Enquiry_Year=df_filtered["AMT_REQ_CREDIT_BUREAU_YEAR"] > 0,
            Has_Social_Default_30=df_filtered["DEF_30_CNT_SOCIAL_CIRCLE"] > 0,
        )

        metrics = calc_kpis(df_filtered)
        social = get_social_circle_kpis(df_filtered)

        cols = st.columns(5)
        cols[0].metric("Total Applicants", f"{metrics['total_applicants']:,}")
        cols[1].metric("Default Rate", f"{metrics['default_rate']:.2f}%")
        cols[2].metric("Avg Bureau Enquiries/Year", f"{df_filtered['AMT_REQ_CREDIT_BUREAU_YEAR'].mean():.2f}")
        cols[3].metric("Avg Social Circle Obs (30d)", f"{social['avg_obs_30']:.2f}")
        cols[4].metric("Avg Social Circle Defaults (30d)", f"{social['avg_def_30']:.2f}")

        st.subheader("Credit Bureau Enquiries")
        bureau_kpis = get_credit_bureau_kpis(df_filtered)
        st.plotly_chart(bar_chart(bureau_kpis, "Period", "Avg Enquiries",
                                   "Avg Credit Bureau Enquiries by Time Window", pre_aggregated=True))
        st.plotly_chart(histogram(df_filtered, "AMT_REQ_CREDIT_BUREAU_YEAR",
                                   "Enquiries in Last Year - Distribution by Risk", color_col="RISK_LABEL"))

        bureau_flag_summary = get_segment_summary(df_filtered, "Has_Bureau_Enquiry_Year")
        st.plotly_chart(bar_chart(bureau_flag_summary, "Has_Bureau_Enquiry_Year", "Default_Rate",
                                   "Default Rate % - Any Bureau Enquiry in Last Year", pre_aggregated=True))

        st.divider()
        st.subheader("Social Circle Default History")

        st.plotly_chart(bar_chart(df_filtered, "DEF_30_CNT_SOCIAL_CIRCLE", None,
                                   "Applicants by Social Circle Defaults (30d)", top_n=8))

        social_flag_summary = get_segment_summary(df_filtered, "Has_Social_Default_30")
        st.plotly_chart(bar_chart(social_flag_summary, "Has_Social_Default_30", "Default_Rate",
                                   "Default Rate % - Any Social Circle Default (30d)", pre_aggregated=True))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
