# 🍽️ DineSight Restaurant Analytics Dashboard

### 🚀 Live Demo
**Click here to view the dashboard:** [PASTE YOUR STREAMLIT APP LINK HERE]

---

## 📖 Project Overview
**Scenario:**
As a data analyst for **DineSight Analytics Pvt. Ltd.**, I was tasked with analyzing restaurant order data to help a food delivery platform improve its operations. The goal of this dashboard is to provide actionable insights into customer ordering patterns and restaurant performance to assist with marketing and delivery planning.

**Objectives:**
* Analyze large datasets of order details and restaurant information.
* Identify top-performing restaurants and bestselling cuisines.
* Determine peak ordering times to optimize delivery logistics.
* Build an interactive, user-friendly dashboard using Python and Streamlit.

---

## 📊 Business Questions & Insights
This dashboard answers the following key business questions identified during the research phase:

1.  **Who are the market leaders?**
    * *Visualization:* A bar chart displaying the Top 10 Restaurants by Total Revenue.
    * *Insight:* Helps identify high-value partners.
2.  **What are customers eating?**
    * *Visualization:* A pie chart showing the market share of different Cuisines.
    * *Insight:* Useful for understanding customer preferences and trends.
3.  **When is the busiest time?**
    * *Visualization:* A heatmap showing order intensity by "Hour of Day" and "Day of Week".
    * *Insight:* Critical for delivery driver allocation and staffing.
4.  **How is the business growing?**
    * *Visualization:* A time-series line chart tracking daily order volumes.
    * *Insight:* Monitors growth trends and seasonal spikes.
5.  **Who are the top customers?**
    * *Visualization:* A leaderboard table of customers with the most orders.
    * *Insight:* Identifies loyal customers for potential rewards programs.

---

## 🛠️ Technical Implementation
This project was built using **Python** and deployed via **Streamlit Cloud**.

### Data Processing (ETL)
* **Data Sources:** Two CSV datasets (`Order_Details.csv` and `Restaurant_Info.csv`).
* **Data Integration:** Merged the two datasets using the `Restaurant_ID` as the primary key.
* **Data Cleaning:**
    * Handled missing values in the Order ID column.
    * Converted `Order Date` strings into datetime objects for time-series analysis.
    * Derived new features: `Hour` and `Day_Name` for the heatmap analysis.

### Technologies Used
* **Streamlit:** For the interactive web interface.
* **Pandas:** For data manipulation, merging, and cleaning.
* **Plotly Express:** For creating interactive, dynamic charts.

---

## ⚙️ How to Run Locally
To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [PASTE YOUR GITHUB REPO LINK HERE]
    ```
2.  **Install requirements:**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

---

