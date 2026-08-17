import pandas as pd


def calc_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_applicants": 0,
            "default_rate": 0.0,
            "avg_income": 0.0,
            "avg_credit": 0.0,
            "avg_annuity": 0.0,
            "avg_age": 0.0,
            "avg_credit_income_ratio": 0.0,
        }
    return {
        "total_applicants": df["SK_ID_CURR"].nunique(),
        "default_rate": df["TARGET"].mean() * 100,
        "avg_income": df["AMT_INCOME_TOTAL"].mean(),
        "avg_credit": df["AMT_CREDIT"].mean(),
        "avg_annuity": df["AMT_ANNUITY"].mean(),
        "avg_age": df["AGE_YEARS"].mean(),
        "avg_credit_income_ratio": df["CREDIT_INCOME_RATIO"].mean(),
    }


def risk_snapshot(df: pd.DataFrame, min_count: int = 30) -> dict:
    """Highest/lowest-risk categories for a few headline dimensions, ignoring any category
    with fewer than min_count applicants - otherwise a tiny category (e.g. 5 "Maternity leave"
    applicants) can produce a noisy 100%-or-0% default rate that looks like a real signal."""
    empty_result = {
        "highest_risk_education": None,
        "lowest_risk_education": None,
        "highest_risk_income_type": None,
        "highest_risk_family_status": None,
    }
    if df.empty:
        return empty_result

    def _safe_extreme(group_col: str, mode: str):
        counts = df.groupby(group_col)["TARGET"].count()
        rates = df.groupby(group_col)["TARGET"].mean()
        valid_rates = rates[counts >= min_count]
        if valid_rates.empty:
            return None
        return valid_rates.idxmax() if mode == "max" else valid_rates.idxmin()

    return {
        "highest_risk_education": _safe_extreme("NAME_EDUCATION_TYPE", "max"),
        "lowest_risk_education": _safe_extreme("NAME_EDUCATION_TYPE", "min"),
        "highest_risk_income_type": _safe_extreme("NAME_INCOME_TYPE", "max"),
        "highest_risk_family_status": _safe_extreme("NAME_FAMILY_STATUS", "max"),
    }


def get_segment_summary(df: pd.DataFrame, group_col: str, top_n: int = None) -> pd.DataFrame:
    """Generic dimension breakdown: applicant count, default rate %, and average financials
    per unique value of group_col. Reused across Demographics, Employment, Housing/Region,
    and Default Risk Analysis pages with a different group_col each time."""
    result = df.groupby(group_col).agg(
        Applicants=("SK_ID_CURR", "nunique"),
        Default_Rate=("TARGET", lambda x: x.mean() * 100),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean"),
    ).reset_index()
    result = result.sort_values("Applicants", ascending=False)
    if top_n:
        result = result.head(top_n)
    return result


def get_risk_driver_ranking(df: pd.DataFrame, dimensions: list, min_count: int = 30) -> pd.DataFrame:
    """For each dimension, the spread (max - min) of default rate % across its categories -
    a rough measure of how much that single dimension differentiates risk. Ranking these lets
    you see which factor matters most without eyeballing a dozen separate bar charts.

    Categories with fewer than min_count applicants are excluded before computing the spread -
    otherwise a handful of tiny categories (e.g. 5 "Maternity leave" applicants) produce a wildly
    noisy default rate that swamps genuinely meaningful differences from larger categories."""
    rows = []
    for dim in dimensions:
        counts = df.groupby(dim)["TARGET"].count()
        rates = df.groupby(dim)["TARGET"].mean() * 100
        valid_rates = rates[counts >= min_count]
        if len(valid_rates) > 1:
            rows.append({"Dimension": dim, "Spread": valid_rates.max() - valid_rates.min()})
    result = pd.DataFrame(rows, columns=["Dimension", "Spread"])
    return result.sort_values("Spread", ascending=False)


def get_credit_bureau_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Average number of Credit Bureau enquiries per time window before application."""
    period_cols = {
        "AMT_REQ_CREDIT_BUREAU_HOUR": "Hour",
        "AMT_REQ_CREDIT_BUREAU_DAY": "Day",
        "AMT_REQ_CREDIT_BUREAU_WEEK": "Week",
        "AMT_REQ_CREDIT_BUREAU_MON": "Month",
        "AMT_REQ_CREDIT_BUREAU_QRT": "Quarter",
        "AMT_REQ_CREDIT_BUREAU_YEAR": "Year",
    }
    avg_enquiries = df[list(period_cols.keys())].mean().rename(index=period_cols)
    return avg_enquiries.reset_index().rename(columns={"index": "Period", 0: "Avg Enquiries"})


def get_social_circle_kpis(df: pd.DataFrame) -> dict:
    """Summary of how many people in the applicant's social circle have observable/defaulted
    30- and 60-day-past-due credit history."""
    return {
        "avg_obs_30": df["OBS_30_CNT_SOCIAL_CIRCLE"].mean(),
        "avg_def_30": df["DEF_30_CNT_SOCIAL_CIRCLE"].mean(),
        "avg_obs_60": df["OBS_60_CNT_SOCIAL_CIRCLE"].mean(),
        "avg_def_60": df["DEF_60_CNT_SOCIAL_CIRCLE"].mean(),
    }


def get_numeric_correlations(df: pd.DataFrame, target_col: str = "TARGET", top_n: int = 15) -> pd.DataFrame:
    """Numeric features most correlated (by magnitude) with the TARGET default flag."""
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()[target_col].drop(target_col)
    corr_sorted = corr.reindex(corr.abs().sort_values(ascending=False).index)
    if top_n:
        corr_sorted = corr_sorted.head(top_n)
    return corr_sorted.reset_index().rename(columns={"index": "Feature", target_col: "Correlation"})
