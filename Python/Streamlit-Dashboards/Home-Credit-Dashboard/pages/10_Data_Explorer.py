import pandas as pd
import streamlit as st
from utils.page_helpers import load_home_credit_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.kpis import calc_kpis

# A curated subset rather than all 127 columns - keeps the table readable, and keeps the CSV
# downloads (and the to_csv() encoding behind them) small on a memory-constrained machine.
DISPLAY_COLS = [
    "SK_ID_CURR", "TARGET", "RISK_LABEL", "CODE_GENDER", "NAME_CONTRACT_TYPE",
    "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "NAME_INCOME_TYPE", "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE", "ORGANIZATION_TYPE", "AGE_YEARS", "YEARS_EMPLOYED",
    "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "CREDIT_INCOME_RATIO",
    "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
]

st.set_page_config(page_title="Data Explorer")

st.title("Data Explorer")

try:
    df = load_home_credit_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)

    if df_filtered.empty:
        empty_state()
    else:
        st.subheader("Additional Filters")
        col1, col2 = st.columns(2)
        with col1:
            occupation_options = sorted(df_filtered["OCCUPATION_TYPE"].dropna().unique())
            occupation_filter = st.multiselect("Occupation Type", options=occupation_options, default=occupation_options)
        with col2:
            id_search = st.text_input("Search by SK_ID_CURR (exact or partial)")

        df_explorer = df_filtered
        if occupation_filter:
            df_explorer = df_explorer[df_explorer["OCCUPATION_TYPE"].isin(occupation_filter)]
        if id_search:
            df_explorer = df_explorer[df_explorer["SK_ID_CURR"].astype(str).str.contains(id_search)]

        if df_explorer.empty:
            empty_state()
        else:
            explorer_metrics = calc_kpis(df_explorer)
            cols = st.columns(5)
            cols[0].metric("Total Applicants (Filtered)", f"{calc_kpis(df_filtered)['total_applicants']:,}")
            cols[1].metric("Applicants Shown", f"{explorer_metrics['total_applicants']:,}")
            cols[2].metric("Default Rate (Shown)", f"{explorer_metrics['default_rate']:.2f}%")
            cols[3].metric("Avg Income (Shown)", f"${explorer_metrics['avg_income']:,.0f}")
            cols[4].metric("Avg Credit (Shown)", f"${explorer_metrics['avg_credit']:,.0f}")

            st.divider()
            st.subheader("Applicant Data")
            st.dataframe(df_explorer[DISPLAY_COLS])

            st.divider()
            st.subheader("Export")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download Filtered Data (CSV)",
                    data=df_explorer[DISPLAY_COLS].to_csv(index=False),
                    file_name="home_credit_filtered.csv",
                    mime="text/csv",
                )
            with col2:
                summary_df = pd.DataFrame([explorer_metrics])
                st.download_button(
                    "Download Summary (CSV)",
                    data=summary_df.to_csv(index=False),
                    file_name="home_credit_summary.csv",
                    mime="text/csv",
                )

except FileNotFoundError:
    st.error("Dataset file not found. Add `data/application_train.csv`.")
