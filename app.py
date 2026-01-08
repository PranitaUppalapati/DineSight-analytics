import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="DineSight Analytics", layout="wide")

st.title("🍽️ DineSight Restaurant Performance Dashboard")
st.markdown("""
This dashboard analyzes customer ordering patterns and restaurant performance 
to improve marketing and delivery planning.
""")

# --- STAGE 2: DATA LOADING & CLEANING [cite: 14, 15, 16] ---
@st.cache_data
def load_and_clean_data():
    # 1. Load Data
    # REPLACE the filenames below with your actual CSV file names
    try:
        def read_table(path_str):
            path = Path(path_str)
            suffix = path.suffix.lower()
            if suffix in [".xlsx", ".xls"]:
                return pd.read_excel(path)
            return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")

        orders = read_table("Order_Details.xlsx")
        restaurants = read_table("Restaurant_Info.xlsx")
    except FileNotFoundError:
        st.error("Data files not found. Please ensure 'Order_Details.xlsx' and 'Restaurant_Info.xlsx' are in the same folder.")
        st.stop()

    # Standardize column names to make merges and references consistent.
    def normalize_columns(df):
        df = df.copy()
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace(r"[()]", "", regex=True)
            .str.replace(r"[-\s]+", "_", regex=True)
        )
        df = df.rename(
            columns={
                "RestaurantID": "Restaurant_ID",
                "RestaurantName": "Restaurant_Name",
            }
        )
        return df

    orders = normalize_columns(orders)
    restaurants = normalize_columns(restaurants)
    
    # 2. Merge Datasets [cite: 15]
    # We assume 'Restaurant_ID' is the common column. Change if different.
    df = pd.merge(orders, restaurants, on="Restaurant_ID", how="left")
    
    # 3. Handle Missing Values 
    df.dropna(subset=['Order_ID'], inplace=True)
    
    # 4. Correct Data Types 
    # Check if your date column is named 'Order Date', 'Date', or 'Order_Date'
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"])
        
    # Create new columns for analysis [cite: 18]
    df["Hour"] = df["Order_Date"].dt.hour
    df["Day_Name"] = df["Order_Date"].dt.day_name()
    
    return df

# Run the data loading function
df = load_and_clean_data()

# --- STAGE 3: BUSINESS METRICS [cite: 12] ---
st.markdown("### Key Performance Indicators")
amount_col = "Order_Amount" if "Order_Amount" in df.columns else "Amount"
if amount_col in df.columns:
    total_sales = df[amount_col].sum()
    formatted_sales = f"${total_sales:,.2f}"
else:
    formatted_sales = "N/A (Order amount column missing)"

total_orders = df['Order_ID'].nunique()
top_rest_name = df['Restaurant_Name'].mode()[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", formatted_sales)
col2.metric("Total Orders", total_orders)
col3.metric("Most Popular Restaurant", top_rest_name)

st.markdown("---")

# --- STAGE 4: INTERACTIVE VISUALIZATIONS [cite: 19] ---

# 1. Top Restaurants (Bar Chart) [cite: 19]
st.subheader("Top Performing Restaurants")
if amount_col in df.columns:
    top_rest = df.groupby("Restaurant_Name")[amount_col].sum().reset_index()
    top_rest = top_rest.sort_values(by=amount_col, ascending=False).head(10)
    fig_bar = px.bar(top_rest, x="Restaurant_Name", y=amount_col,
                     title="Top 10 Restaurants by Revenue",
                     labels={amount_col: "Revenue", "Restaurant_Name": "Restaurant"})
    st.plotly_chart(fig_bar, use_container_width=True)

# 2. Cuisine Popularity (Pie Chart) [cite: 19] & Top Customers [cite: 13]
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Cuisine Market Share")
    if 'Cuisine' in df.columns:
        cuisine_df = df['Cuisine'].value_counts().reset_index()
        cuisine_df.columns = ['Cuisine', 'Orders']
        fig_pie = px.pie(cuisine_df.head(10), values='Orders', names='Cuisine', 
                         title="Top 10 Cuisines by Orders")
        st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Top Customers")
    # This answers the "Who are the top customers?" question [cite: 13]
    if 'Customer_Name' in df.columns:
        top_cust = df['Customer_Name'].value_counts().reset_index().head(10)
        top_cust.columns = ['Customer Name', 'Total Orders']
        st.dataframe(top_cust, use_container_width=True)
    elif 'Customer_ID' in df.columns:
        top_cust = df['Customer_ID'].value_counts().reset_index().head(10)
        top_cust.columns = ['Customer ID', 'Total Orders']
        st.dataframe(top_cust, use_container_width=True)
    else:
        st.info("Customer column not found.")

# 3. Order Trends (Time Series) [cite: 19]
st.subheader("Daily Order Trends")
date_counts = df["Order_Date"].dt.date.nunique()
if date_counts < 2:
    st.info("Only one order date found. Showing hourly trend instead.")
    hourly_orders = (
        df.groupby(df["Order_Date"].dt.floor("H"))
        .size()
        .reset_index(name="Orders")
        .rename(columns={"Order_Date": "DateTime"})
    )
    fig_line = px.line(hourly_orders, x="DateTime", y="Orders", title="Order Volume Over Time")
else:
    daily_orders = (
        df.groupby(df["Order_Date"].dt.date)
        .size()
        .reset_index(name="Orders")
        .rename(columns={"Order_Date": "Date"})
    )
    fig_line = px.line(daily_orders, x="Date", y="Orders", title="Order Volume Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# 4. Peak Hours Heatmap [cite: 19]
st.subheader("Peak Ordering Times")
heatmap_data = df.groupby(['Day_Name', 'Hour']).size().reset_index(name='Orders')
# Pivot the data for the heatmap format
heatmap_pivot = heatmap_data.pivot(index='Day_Name', columns='Hour', values='Orders').fillna(0)

# Sort days logically
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_pivot = heatmap_pivot.reindex(days_order)

fig_heat = px.imshow(heatmap_pivot, 
                     labels=dict(x="Hour of Day", y="Day of Week", color="Order Count"),
                     title="Heatmap of Busy Hours")
st.plotly_chart(fig_heat, use_container_width=True)
