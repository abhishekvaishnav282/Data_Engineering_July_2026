import pandas as pd


def calc_kpis(df: pd.DataFrame) -> dict:
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()
    total_quantity = df["Quantity"].sum()
    profit_margin = total_profit / total_sales * 100 if total_sales else 0.0
    avg_order_value = total_sales / total_orders if total_orders else 0.0
    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_quantity": total_quantity,
        "profit_margin": profit_margin,
        "avg_order_value": avg_order_value,
    }


def top_bottom_summary(df: pd.DataFrame) -> dict:
    return {
        "best_region_sales": df.groupby("Region")["Sales"].sum().idxmax() if not df.empty else None,
        "best_category_sales": df.groupby("Category")["Sales"].sum().idxmax() if not df.empty else None,
        "highest_sales_month": df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().idxmax().strftime("%Y-%m") if not df.empty else None,
        "highest_profit_month": df.groupby(df["Order Date"].dt.to_period("M"))["Profit"].sum().idxmax().strftime("%Y-%m") if not df.empty else None,
    }


def get_regional_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by region"""
    return df.groupby("Region").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
        "Customer ID": "nunique",
        "Quantity": "sum",
    }).rename(columns={
        "Order ID": "Orders",
        "Customer ID": "Customers",
    }).reset_index()


def get_state_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by state"""
    return df.groupby("State").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
        "Customer ID": "nunique",
        "Quantity": "sum",
    }).rename(columns={
        "Order ID": "Orders",
        "Customer ID": "Customers",
    }).reset_index().sort_values("Sales", ascending=False)


def get_city_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by city"""
    return df.groupby(["City", "State"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
        "Customer ID": "nunique",
        "Quantity": "sum",
    }).rename(columns={
        "Order ID": "Orders",
        "Customer ID": "Customers",
    }).reset_index().sort_values("Sales", ascending=False)


def get_category_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by category"""
    result = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique",
    }).rename(columns={
        "Order ID": "Orders",
    }).reset_index()
    result["Profit Margin %"] = (result["Profit"] / result["Sales"] * 100).round(2)
    return result.sort_values("Sales", ascending=False)


def get_subcategory_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by sub-category"""
    result = df.groupby("Sub-Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean",
    }).rename(columns={
        "Discount": "Avg Discount",
    }).reset_index()
    result["Profit Margin %"] = (result["Profit"] / result["Sales"] * 100).round(2)
    return result.sort_values("Sales", ascending=False)


def get_product_kpis(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """Get KPIs by product"""
    result = df.groupby(["Product Name", "Category", "Sub-Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean",
    }).rename(columns={
        "Discount": "Avg Discount",
    }).reset_index()
    result["Profit Margin %"] = (result["Profit"] / result["Sales"] * 100).round(2)
    result = result.sort_values("Sales", ascending=False)
    if top_n:
        result = result.head(top_n)
    return result


def get_customer_kpis(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """Get KPIs by customer"""
    result = df.groupby(["Customer Name", "Customer ID", "Segment"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique",
    }).rename(columns={
        "Order ID": "Orders",
    }).reset_index()
    result = result.sort_values("Sales", ascending=False)
    if top_n:
        result = result.head(top_n)
    return result


def get_segment_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by customer segment"""
    result = df.groupby("Segment").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique",
        "Customer ID": "nunique",
        "Discount": "mean",
    }).rename(columns={
        "Order ID": "Orders",
        "Customer ID": "Customers",
        "Discount": "Avg Discount",
    }).reset_index()
    result["Profit Margin %"] = (result["Profit"] / result["Sales"] * 100).round(2)
    return result


def get_order_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by order"""
    order_df = df.groupby("Order ID").agg({
        "Order Date": "first",
        "Customer Name": "first",
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
    }).reset_index()
    order_df["Avg Profit per Order"] = order_df["Profit"] / order_df.groupby("Order ID").size()
    return order_df.sort_values("Order Date", ascending=False)


def get_shipping_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Get KPIs by ship mode"""
    result = df.groupby("Ship Mode").agg({
        "Order ID": "nunique",
        "Sales": "sum",
        "Profit": "sum",
        "Shipping Days": "mean",
    }).rename(columns={
        "Order ID": "Shipments",
        "Shipping Days": "Avg Shipping Days",
    }).reset_index()
    return result


def get_loss_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Get loss-making records"""
    loss_df = df[df["Profit"] < 0].copy()
    return loss_df.sort_values("Profit", ascending=True)


def get_discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze discount impact"""
    df_copy = df.copy()
    df_copy["Discount_Range"] = pd.cut(
        df_copy["Discount"],
        bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1.0],
        labels=["0%", "1-10%", "11-20%", "21-30%", "31-50%", "51%+"],
    )
    return df_copy.groupby("Discount_Range", observed=True).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
    }).rename(columns={
        "Order ID": "Orders",
    }).reset_index()


def get_growth_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate month-over-month growth metrics"""
    df_copy = df.copy()
    df_copy["YearMonth"] = df_copy["Order Date"].dt.to_period("M")
    monthly = df_copy.groupby("YearMonth").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
    }).rename(columns={
        "Order ID": "Orders",
    }).reset_index()
    
    monthly["Sales_Growth_%"] = monthly["Sales"].pct_change() * 100
    monthly["Profit_Growth_%"] = monthly["Profit"].pct_change() * 100
    return monthly
