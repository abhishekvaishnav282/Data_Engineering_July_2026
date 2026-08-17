import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_segment_summary
from utils.charts import bar_chart, histogram

st.set_page_config(page_title="Housing & Region Analysis")

st.title("Housing & Region Analysis")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        pct_own_car = (df_filtered["FLAG_OWN_CAR"] == "Y").mean() * 100
        pct_own_realty = (df_filtered["FLAG_OWN_REALTY"] == "Y").mean() * 100

        cols = st.columns(5)
        cols[0].metric("Total Applicants", f"{metrics['total_applicants']:,}")
        cols[1].metric("Default Rate", f"{metrics['default_rate']:.2f}%")
        cols[2].metric("Own Car", f"{pct_own_car:.1f}%")
        cols[3].metric("Own Realty", f"{pct_own_realty:.1f}%")
        cols[4].metric("Avg Region Rating", f"{df_filtered['REGION_RATING_CLIENT'].mean():.2f}")

        st.plotly_chart(bar_chart(df_filtered, "NAME_HOUSING_TYPE", None, "Applicants by Housing Type"))

        housing_summary = get_segment_summary(df_filtered, "NAME_HOUSING_TYPE")
        st.plotly_chart(bar_chart(housing_summary, "NAME_HOUSING_TYPE", "Default_Rate",
                                   "Default Rate % by Housing Type", pre_aggregated=True))

        car_summary = get_segment_summary(df_filtered, "FLAG_OWN_CAR")
        st.plotly_chart(bar_chart(car_summary, "FLAG_OWN_CAR", "Default_Rate",
                                   "Default Rate % by Car Ownership", pre_aggregated=True))

        realty_summary = get_segment_summary(df_filtered, "FLAG_OWN_REALTY")
        st.plotly_chart(bar_chart(realty_summary, "FLAG_OWN_REALTY", "Default_Rate",
                                   "Default Rate % by Realty Ownership", pre_aggregated=True))

        region_summary = get_segment_summary(df_filtered, "REGION_RATING_CLIENT")
        st.plotly_chart(bar_chart(region_summary, "REGION_RATING_CLIENT", "Default_Rate",
                                   "Default Rate % by Region Rating", pre_aggregated=True))

        st.plotly_chart(histogram(df_filtered, "TOTALAREA_MODE", "Total Area (normalized) Distribution by Risk", color_col="RISK_LABEL"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
