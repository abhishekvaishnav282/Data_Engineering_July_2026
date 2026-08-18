import pandas as pd


def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_excel(csv_path, parse_dates=["Order Date", "Ship Date"])
    # Standardize column names
    df.columns = [col.strip() for col in df.columns]
    if "Profit Margin" not in df.columns:
        df["Profit Margin"] = df["Profit"] / df["Sales"] * 100
    if "Shipping Days" not in df.columns and "Order Date" in df.columns and "Ship Date" in df.columns:
        df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df
