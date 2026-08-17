import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis, get_numeric_correlations
from utils.charts import horizontal_bar_chart, heatmap

st.set_page_config(page_title="Correlation Explorer")

st.title("Correlation Explorer")
st.caption("Numeric applicant attributes ranked by how strongly they correlate with TARGET (default). "
           "Correlation is not causation - this shows association, not proof that a feature drives risk.")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        metrics = calc_kpis(df_filtered)
        top_n = st.slider("Number of top correlated features to show", min_value=5, max_value=30, value=15)
        corr_df = get_numeric_correlations(df_filtered, top_n=top_n)
        top_feature = corr_df.iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Applicants", f"{metrics['total_applicants']:,}")
        col2.metric("Default Rate", f"{metrics['default_rate']:.2f}%")
        col3.metric("Strongest Predictor", top_feature["Feature"], delta=f"{top_feature['Correlation']:.3f}")

        st.plotly_chart(horizontal_bar_chart(corr_df, "Feature", "Correlation",
                                              f"Top {top_n} Features Correlated with Default", pre_aggregated=True))

        st.subheader("Correlation Heatmap")
        st.caption(f"Pairwise correlation among the top {top_n} features plus TARGET - "
                   "useful for spotting features that are redundant with each other, not just with TARGET.")
        pivot = df_filtered[list(corr_df["Feature"]) + ["TARGET"]].corr()
        st.plotly_chart(heatmap(pivot, f"Correlation Heatmap (Top {top_n} Features + TARGET)"))

        st.dataframe(corr_df)

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
