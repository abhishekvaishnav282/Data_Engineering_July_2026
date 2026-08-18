import streamlit as st
from utils.page_helpers import load_superstore_data, empty_state
from utils.filters import sidebar_filters, apply_filters
from utils.charts import bar_chart, horizontal_bar_chart

st.set_page_config(page_title="Top & Bottom Performers")

st.title("Top & Bottom Performers")

try:
    df = load_superstore_data()
    filters = sidebar_filters(df)
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        empty_state()
    else:
        # Filter for Top N / Bottom N
        n_options = [5, 10, 20]
        selected_n = st.selectbox("Select number of items to display:", n_options, index=1)
        
        st.subheader("TOP PERFORMERS")
        
        # Top Products by Sales
        top_prod_sales = df_filtered.groupby("Product Name")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_prod_sales, "Product Name", "Sales", f"Top {selected_n} Products by Sales"), use_container_width=True)
        
        # Top Products by Profit
        top_prod_profit = df_filtered.groupby("Product Name")["Profit"].sum().reset_index().sort_values("Profit", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_prod_profit, "Product Name", "Profit", f"Top {selected_n} Products by Profit"), use_container_width=True)
        
        # Top Customers by Sales
        top_cust_sales = df_filtered.groupby("Customer Name")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_cust_sales, "Customer Name", "Sales", f"Top {selected_n} Customers by Sales"), use_container_width=True)
        
        # Top Customers by Profit
        top_cust_profit = df_filtered.groupby("Customer Name")["Profit"].sum().reset_index().sort_values("Profit", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_cust_profit, "Customer Name", "Profit", f"Top {selected_n} Customers by Profit"), use_container_width=True)
        
        # Top States by Sales
        top_state_sales = df_filtered.groupby("State")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_state_sales, "State", "Sales", f"Top {selected_n} States by Sales"), use_container_width=True)
        
        # Top Cities by Sales
        top_city_sales = df_filtered.groupby("City")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(selected_n)
        st.plotly_chart(bar_chart(top_city_sales, "City", "Sales", f"Top {selected_n} Cities by Sales"), use_container_width=True)
        
        st.subheader("BOTTOM PERFORMERS")
        
        # Bottom Products by Profit
        bottom_prod_profit = df_filtered.groupby("Product Name")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(selected_n)
        st.plotly_chart(
            horizontal_bar_chart(bottom_prod_profit, "Product Name", "Profit", f"Bottom {selected_n} Products by Profit"),
            use_container_width=True
        )
        
        # Bottom Customers by Profit
        bottom_cust_profit = df_filtered.groupby("Customer Name")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(selected_n)
        st.plotly_chart(
            horizontal_bar_chart(bottom_cust_profit, "Customer Name", "Profit", f"Bottom {selected_n} Customers by Profit"),
            use_container_width=True
        )
        
        # Bottom States by Profit
        bottom_state_profit = df_filtered.groupby("State")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(selected_n)
        st.plotly_chart(
            horizontal_bar_chart(bottom_state_profit, "State", "Profit", f"Bottom {selected_n} States by Profit"),
            use_container_width=True
        )
        
        # Bottom Cities by Profit
        bottom_city_profit = df_filtered.groupby("City")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(selected_n)
        st.plotly_chart(
            horizontal_bar_chart(bottom_city_profit, "City", "Profit", f"Bottom {selected_n} Cities by Profit"),
            use_container_width=True
        )
        
        # Bottom Sub-Categories by Profit
        bottom_subcat_profit = df_filtered.groupby("Sub-Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).head(selected_n)
        st.plotly_chart(
            horizontal_bar_chart(bottom_subcat_profit, "Sub-Category", "Profit", f"Bottom {selected_n} Sub-Categories by Profit"),
            use_container_width=True
        )
        
except FileNotFoundError:
    st.error("Dataset file not found. Add `data/sample_superstore.csv`.")
