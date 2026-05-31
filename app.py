import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Unique Page Styling
st.set_page_config(page_title="Nexus Retail Engine", layout="wide")

# Custom CSS to make it look different (Dark Mode feel)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - This is where your AI will live!
with st.sidebar:
    st.title("🤖 AI Command Center")
    
    # --- NEW DATE CARD START ---
    st.markdown("""
        <div style="background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 20px;">
            <p style="color: #9ca3af; margin: 0; font-size: 14px; text-transform: uppercase;">Reporting Period</p>
            <h2 style="color: #ffffff; margin: 0; font-size: 24px;">December 2010</h2>
            <p style="color: #00d4ff; margin: 0; font-size: 14px;">Live Snapshot: Dec 01</p>
        </div>
    """, unsafe_allow_html=True)


    # --- NEW DATE CARD END ---
    
    st.info("AI Model Status: Standing by...")
    st.divider()
    st.write("Welcome, Lead Developer. Use this panel to interact with the predictive engine.")


# --- MAIN HEADER SECTION ---
# This adds a professional icon and your unique brand name
st.title(" Nexus Retail: Strategic Intelligence")
st.caption(f"Real-time analysis for December 2010 | System synced at {datetime.now().strftime('%H:%M:%S')}")

# Add a little professional "Welcome" message
st.markdown("""
    <div style="background-color: #1f2937; padding: 10px 20px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 25px;">
        <span style="color: #9ca3af; font-size: 14px;">Operational Mode:</span> 
        <b style="color: #90D5FF;">Live Inventory Tracking</b> 
    </div>
""", unsafe_allow_html=True)


# 3. Secure Database Connection
def fetch_retail_records():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("Successfully connected to Nexus Database")

            sql_query = "SELECT * FROM dashboard_sales_data"
            data_frame = pd.read_sql(sql_query, connection)

            connection.close()
            return data_frame
        else:
            st.error("Database Sync Failed: could not establish connection.")
            return None
    except Exception as error:
        st.error(f"Database Sync Failed: {error}")
        return None


# 4. Processing & Display
# (DB connection code kept exactly as-is above.)

raw_data = fetch_retail_records()

if raw_data is None or getattr(raw_data, "empty", True):
    st.warning("No data loaded yet. Please confirm MySQL is running and table `dashboard_sales_data` has rows.")
    st.stop()

# --- DATA CLEANING ---
raw_data["TotalAmount"] = pd.to_numeric(raw_data.get("TotalAmount"), errors="coerce")
raw_data["SalesHour"] = pd.to_numeric(raw_data.get("SalesHour"), errors="coerce")

with st.sidebar:
    st.subheader(" Predictive Intelligence")
    if st.button(" Forecast Remaining Day"):
        st.info("Analyzing hourly velocity...")
        hourly_data = (
            raw_data.groupby("SalesHour")["TotalAmount"]
            .sum()
            .reset_index()
            .dropna(subset=["SalesHour", "TotalAmount"])
        )
        if hourly_data.empty:
            st.warning("Not enough hourly data to forecast.")
        else:
            X = hourly_data["SalesHour"].values.reshape(-1, 1)
            y = hourly_data["TotalAmount"].values
            model = LinearRegression().fit(X, y)
            prediction = model.predict([[13]])  # 1 PM
            st.success(f"Predicted 1 PM Volume: £{prediction[0]:,.2f}")
    else:
        st.info("AI Model Status: Standing by...")

# --- TOP ROW: KPI METRICS ---
col1, col2, col3 = st.columns(3)
total_rev = float(np.nan_to_num(raw_data["TotalAmount"].sum(), nan=0.0))
unique_inv = int(raw_data.get("InvoiceNo", pd.Series(dtype=object)).nunique())
customer_reach = int(raw_data.get("CustomerID", pd.Series(dtype=object)).nunique())

col1.metric("Gross Revenue", f"£{total_rev:,.2f}")
col2.metric("Transaction Volume", f"{unique_inv:,}")
col3.metric("Client Base", f"{customer_reach:,}")

st.divider()

# --- MIDDLE ROW: TRENDS & GEOGRAPHY ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader(" Strategic Revenue Mix")
    if "SalesCategory" in raw_data.columns:
        category_dist = (
            raw_data.groupby("SalesCategory")["TotalAmount"]
            .sum()
            .reset_index()
            .sort_values("TotalAmount", ascending=False)
        )
        if category_dist.empty:
            st.info("No category data available.")
        else:
            fig_donut = px.pie(
                category_dist,
                values="TotalAmount",
                names="SalesCategory",
                hole=0.5,
                template="plotly_dark",
                color_discrete_sequence=["#00d4ff", "#ffaa00"],
            )
            fig_donut.update_traces(textposition="inside", textinfo="percent+label")
            fig_donut.update_layout(showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)
            top_cat = category_dist.iloc[0]["SalesCategory"]
            st.write(f"**Insight:** Most of today's revenue is driven by **{top_cat}** transactions.")
    else:
        st.info("Missing `SalesCategory` column.")

with chart_col2:
    st.subheader("Global Market Share")
    if "Country" in raw_data.columns:
        country_rev = (
            raw_data.groupby("Country")["TotalAmount"]
            .sum()
            .reset_index()
            .sort_values("TotalAmount", ascending=False)
            .head(10)
        )
        if country_rev.empty:
            st.info("No country data available.")
        else:
            fig_country = px.bar(
                country_rev,
                x="TotalAmount",
                y="Country",
                orientation="h",
                template="plotly_dark",
                color="TotalAmount",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.info("Missing `Country` column.")

# --- BOTTOM ROW: PRODUCTS & TIME ---
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader(" Elite Inventory (Top 10)")
    if "Description" in raw_data.columns:
        top_products = (
            raw_data.groupby("Description")["TotalAmount"]
            .sum()
            .reset_index()
            .sort_values("TotalAmount", ascending=False)
            .head(10)
        )
        if top_products.empty:
            st.info("No product data available.")
        else:
            fig_products = px.pie(top_products, values="TotalAmount", names="Description", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_products, use_container_width=True)
    else:
        st.info("Missing `Description` column.")

with chart_col4:
    st.subheader(" Operational Peak Hours")
    if "SalesHour" in raw_data.columns:
        hourly_sales = (
            raw_data.groupby("SalesHour")["TotalAmount"]
            .sum()
            .reset_index()
            .dropna(subset=["SalesHour", "TotalAmount"])
        )
        if hourly_sales.empty:
            st.info("No hourly data available.")
        else:
            fig_hour = px.area(hourly_sales, x="SalesHour", y="TotalAmount", template="plotly_dark", color_discrete_sequence=["#ffaa00"])
            st.plotly_chart(fig_hour, use_container_width=True)
    else:
        st.info("Missing `SalesHour` column.")

st.divider()

# --- NEW VIP SECTION ---
st.subheader("🏆 Daily Customer Leaderboard")
if "CustomerID" in raw_data.columns:
    top_customers = (
        raw_data.groupby("CustomerID")["TotalAmount"]
        .sum()
        .reset_index()
        .sort_values("TotalAmount", ascending=False)
        .head(5)
    )
    c_vip1, c_vip2, c_vip3, c_vip4, c_vip5 = st.columns(5)
    vips = [c_vip1, c_vip2, c_vip3, c_vip4, c_vip5]
    for i, row in enumerate(top_customers.itertuples(index=False)):
        vips[i].metric(f"VIP #{i+1}", f"ID: {row.CustomerID}", f"£{row.TotalAmount:,.2f}")
else:
    st.info("Missing `CustomerID` column.")

# --- THE NEXUS CONSULTANT BOT SECTION ---
st.divider()
st.subheader("💬 Nexus Data Consultant")
st.info("Ask about: revenue, best product, predict/forecast, trend, country, best hour, average/AOV, VIP, category.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Analyze our performance...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_low = prompt.lower()
    response = None
#1

    if response is None and ("predict" in prompt_low or "forecast" in prompt_low):
        if "SalesHour" in raw_data.columns:
            hourly_data = raw_data.groupby("SalesHour")["TotalAmount"].sum().reset_index().dropna()
            if len(hourly_data) < 2:
                response = "Nexus AI: I need more data points to build a reliable forecast."
            else:
                last_hour = int(hourly_data['SalesHour'].max())
                next_hour = last_hour + 1
                model = LinearRegression().fit(hourly_data[["SalesHour"]], hourly_data["TotalAmount"])
                pred = model.predict([[next_hour]])[0]
                response = (f"Nexus AI: The latest data record is from {last_hour}:00. "
                            f"Based on the trend, I forecast **£{max(0, pred):,.2f}** for the next business hour ({next_hour}:00).")
   #2
    if response is None and ("best" in prompt_low and "hour" in prompt_low):
        best_hour = raw_data.groupby("SalesHour")["TotalAmount"].sum().idxmax()
        response = f"Nexus Bot: Our 'Golden Hour' (highest performance) is **{best_hour}:00**."

    #3
    # Best Item
    if response is None and ("best" in prompt_low or "top" in prompt_low) and ("item" in prompt_low or "product" in prompt_low) and "country" not in prompt_low:
        item_sales = raw_data.groupby("Description")["TotalAmount"].sum()
        top_item = item_sales.idxmax()
        top_amt = item_sales.max()
        response = (f"Nexus Insight : **'{top_item}'** is currently the strongest-performing product, "
                    f"generating **£{top_amt:,.2f}** in revenue. This item contributes more revenue "
                    f"than any other product in the catalog and is a key sales driver.")
        #3
    elif response is None and ("least" in prompt_low or "worst" in prompt_low or "lowest" in prompt_low) and ("item" in prompt_low or "product" in prompt_low):
        item_sales = raw_data.groupby("Description")["TotalAmount"].sum()
        low_item = item_sales.idxmin()
        low_amt = item_sales.min()
        response = (f"Nexus Insight : **'{low_item}'** is the lowest-performing product, "
                    f"bringing in only **£{low_amt:,.2f}**. This product may require a pricing, "
                    f"marketing, or inventory review.")
        
    #4
    # Worst Country first for prompts like "least selling country"
    if response is None and "country" in prompt_low and ("least" in prompt_low or "worst" in prompt_low or "lowest" in prompt_low):
        country_sales = raw_data.groupby("Country")["TotalAmount"].sum()
        low_country = country_sales.idxmin()
        low_amt = country_sales.min()
        response = (f"Nexus Market Analysis : **{low_country}** records the lowest revenue at **£{low_amt:,.2f}**. "
                    f"This market currently contributes the least to overall sales and may present "
                    f"growth opportunities or require market exit evaluation.")

    # Best Country (With % Comparison)
    elif response is None and "country" in prompt_low and ("best" in prompt_low or "top" in prompt_low or "selling" in prompt_low):
        country_sales = raw_data.groupby("Country")["TotalAmount"].sum()
        top_country = country_sales.idxmax()
        top_amt = country_sales.max()
        avg_amt = country_sales.mean()
        pct_above = ((top_amt - avg_amt) / avg_amt) * 100 if avg_amt else 0
        
        response = (f"Nexus Market Analysis : **{top_country}** leads all markets with **£{top_amt:,.2f}** in revenue. "
                    f"This is **{pct_above:.1f}% above the average** country performance, "
                    f"highlighting its role as the primary revenue engine.")
        

    elif response is None and "country" in prompt_low:
        top_country = raw_data.groupby("Country")["TotalAmount"].sum().idxmax()
        amt = raw_data.groupby("Country")["TotalAmount"].sum().max()
        response = f"Nexus Bot: The highest sales are happening in **{top_country}**, contributing **£{amt:,.2f}**."

#5    
    if response is None and ("revenue" in prompt_low or "money" in prompt_low or "total" in prompt_low):
        total = float(np.nan_to_num(raw_data["TotalAmount"].sum(), nan=0.0))
        response = f"Nexus Bot: Current gross revenue stands at **£{total:,.2f}**."


    #6
    if response is None and ("customer" in prompt_low or "client" in prompt_low):
        count = int(raw_data["CustomerID"].nunique())
        response = f"Nexus Bot: We have engaged with **{count} unique customers** today."
      #7  

    if response is None and ("average" in prompt_low or "aov" in prompt_low):
        denom = int(raw_data["InvoiceNo"].nunique())
        aov = (float(np.nan_to_num(raw_data["TotalAmount"].sum(), nan=0.0)) / denom) if denom else 0.0
        response = f"Nexus Bot: Our Average Order Value (AOV) is **£{aov:,.2f}** per transaction."

    #8
    if response is None and ("trend" in prompt_low or "growth" in prompt_low):
        hourly_sums = raw_data.groupby("SalesHour")["TotalAmount"].sum().values
        if len(hourly_sums) > 1:
            diff = float(hourly_sums[-1] - hourly_sums[-2])
            status = "UP" if diff > 0 else "DOWN"
            response = f"Nexus AI: The current trend is **{status}**. Revenue changed by £{abs(diff):,.2f} in the last hour."
        else:
            response = "Nexus AI: I need more hourly data to establish a trend line."

            #9
    if response is None and ("vip" in prompt_low or "whale" in prompt_low):
        top_vip = raw_data.groupby("CustomerID")["TotalAmount"].sum().idxmax()
        response = f"Nexus Bot: Our highest-spending VIP is Customer **ID: {top_vip}**."

    #10
    if response is None and ("category" in prompt_low or "type" in prompt_low):
        top_cat = raw_data.groupby("SalesCategory")["TotalAmount"].sum().idxmax()
        response = f"Nexus Bot: The **{top_cat}** category is currently driving the majority of our revenue."

    if response is None:
        response = "Nexus Bot: Try asking about revenue, best product, predict/forecast, trend, country, best hour, AOV, VIP, or category."

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.expander("🔍 System Audit: Raw Data Logs"):
    st.dataframe(raw_data.head(50), use_container_width=True)