import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, risk_snapshot, get_segment_summary, get_risk_driver_ranking
from utils.charts import bar_chart, horizontal_bar_chart

DIMENSIONS = [
    "NAME_CONTRACT_TYPE", "CODE_GENDER", "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS",
    "NAME_INCOME_TYPE", "NAME_HOUSING_TYPE", "OCCUPATION_TYPE", "ORGANIZATION_TYPE",
    "REGION_RATING_CLIENT", "FLAG_OWN_CAR", "FLAG_OWN_REALTY",
]

st.set_page_config(page_title="Default Risk Analysis")

st.title("Default Risk Analysis")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        col1, col2 = st.columns(2)
        col1.metric("Total Applicants", f"{metrics['total_applicants']:,}")
        col2.metric("Overall Default Rate", f"{metrics['default_rate']:.2f}%")

        st.subheader("⚠️ Key Risk Segments")
        snapshot = risk_snapshot(df_filtered)
        c1, c2, c3, c4 = st.columns(4)
        c1.info(f"Highest Risk Education: **{snapshot['highest_risk_education']}**")
        c2.info(f"Lowest Risk Education: **{snapshot['lowest_risk_education']}**")
        c3.info(f"Highest Risk Income Type: **{snapshot['highest_risk_income_type']}**")
        c4.info(f"Highest Risk Family Status: **{snapshot['highest_risk_family_status']}**")

        st.divider()
        st.subheader("Which Factor Differentiates Risk the Most?")
        st.caption("Spread = highest category default rate minus lowest, within each dimension. "
                   "A bigger spread means that dimension separates high-risk from low-risk applicants more sharply.")
        ranking = get_risk_driver_ranking(df_filtered, DIMENSIONS)
        st.plotly_chart(horizontal_bar_chart(ranking, "Dimension", "Spread",
                                              "Default Rate Spread by Dimension", pre_aggregated=True))

        st.divider()
        st.subheader("Drill Into a Dimension")
        selected_dim = st.selectbox("Choose a dimension to break default rate down by:", DIMENSIONS)
        summary = get_segment_summary(df_filtered, selected_dim)
        st.plotly_chart(bar_chart(summary, selected_dim, "Default_Rate",
                                   f"Default Rate % by {selected_dim}", pre_aggregated=True))
        st.dataframe(summary)

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
