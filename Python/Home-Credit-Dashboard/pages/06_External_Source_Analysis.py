import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis
from utils.charts import histogram, box_plot, scatter_chart

st.set_page_config(page_title="External Source Analysis")

st.title("External Source Analysis")
st.caption("EXT_SOURCE_1/2/3 are normalized credit scores from external data sources - "
           "typically the strongest predictors of default in this dataset.")

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
        cols[2].metric("Avg EXT_SOURCE_1", f"{df_filtered['EXT_SOURCE_1'].mean():.3f}")
        cols[3].metric("Avg EXT_SOURCE_2", f"{df_filtered['EXT_SOURCE_2'].mean():.3f}")
        cols[4].metric("Avg EXT_SOURCE_3", f"{df_filtered['EXT_SOURCE_3'].mean():.3f}")

        st.plotly_chart(histogram(df_filtered, "EXT_SOURCE_1", "EXT_SOURCE_1 Distribution by Risk", color_col="RISK_LABEL"))
        st.plotly_chart(histogram(df_filtered, "EXT_SOURCE_2", "EXT_SOURCE_2 Distribution by Risk", color_col="RISK_LABEL"))
        st.plotly_chart(histogram(df_filtered, "EXT_SOURCE_3", "EXT_SOURCE_3 Distribution by Risk", color_col="RISK_LABEL"))

        st.plotly_chart(box_plot(df_filtered, "EXT_SOURCE_2", "RISK_LABEL", "EXT_SOURCE_2 by Risk (Box Plot)"))
        st.plotly_chart(box_plot(df_filtered, "EXT_SOURCE_3", "RISK_LABEL", "EXT_SOURCE_3 by Risk (Box Plot)"))

        sample_df = df_filtered.sample(n=min(2000, len(df_filtered)), random_state=42)
        st.plotly_chart(scatter_chart(sample_df, "EXT_SOURCE_2", "EXT_SOURCE_3", "RISK_LABEL",
                                       "EXT_SOURCE_2 vs EXT_SOURCE_3 (sampled)"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
