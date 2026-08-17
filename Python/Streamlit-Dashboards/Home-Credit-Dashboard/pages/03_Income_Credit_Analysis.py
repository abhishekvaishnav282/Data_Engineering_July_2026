import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis
from utils.charts import histogram, box_plot, scatter_chart

st.set_page_config(page_title="Income & Credit Analysis")

st.title("Income & Credit Analysis")

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
        cols[1].metric("Avg Income", f"${metrics['avg_income']:,.0f}")
        cols[2].metric("Avg Credit", f"${metrics['avg_credit']:,.0f}")
        cols[3].metric("Avg Annuity", f"${metrics['avg_annuity']:,.0f}")
        cols[4].metric("Avg Credit/Income", f"{metrics['avg_credit_income_ratio']:.2f}")

        # AMT_INCOME_TOTAL has a small number of extreme outliers (one applicant reports
        # $117M income) that would otherwise compress this histogram into an unreadable
        # single spike - excluded from this chart's display only, not from the underlying data.
        st.caption("Income histogram below excludes the <0.1% of applicants reporting income above $1M, for readability.")
        income_display_df = df_filtered[df_filtered["AMT_INCOME_TOTAL"] < 1_000_000]
        st.plotly_chart(histogram(income_display_df, "AMT_INCOME_TOTAL", "Income Distribution by Risk", color_col="RISK_LABEL"))

        st.plotly_chart(histogram(df_filtered, "AMT_CREDIT", "Credit Amount Distribution by Risk", color_col="RISK_LABEL"))
        st.plotly_chart(histogram(df_filtered, "AMT_ANNUITY", "Annuity Distribution by Risk", color_col="RISK_LABEL"))
        st.plotly_chart(box_plot(df_filtered, "AMT_CREDIT", "NAME_CONTRACT_TYPE", "Credit Amount by Contract Type"))
        st.plotly_chart(histogram(df_filtered, "CREDIT_INCOME_RATIO", "Credit-to-Income Ratio Distribution by Risk", color_col="RISK_LABEL"))

        sample_df = df_filtered.sample(n=min(2000, len(df_filtered)), random_state=42)
        st.plotly_chart(scatter_chart(sample_df, "AMT_GOODS_PRICE", "AMT_CREDIT", "NAME_CONTRACT_TYPE",
                                       "Goods Price vs Credit Amount (sampled)"))

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
