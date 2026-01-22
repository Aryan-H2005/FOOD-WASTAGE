import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Global Food Waste Analytics",
    layout="wide"
)

st.title("🍽️ Global Food Waste Analytics Dashboard")
st.markdown("Data-driven insights for **policy makers & sustainability teams**")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_global_food_wastage_dataseta.csv")
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Country"].unique()),
    default=df["Country"].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=df["Year"].unique()
)

category = st.sidebar.multiselect(
    "Food Category",
    options=sorted(df["Food Category"].unique()),
    default=df["Food Category"].unique()
)

filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Year"].isin(year)) &
    (df["Food Category"].isin(category))
]

# ---------------- KPI METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

total_waste = filtered_df["Total Waste (Tons)"].sum()
economic_loss = filtered_df["Economic Loss (Million $)"].sum()
avg_per_capita = filtered_df["Avg Waste per Capita (Kg)"].mean()
avg_household = filtered_df["Household Waste (%)"].mean()

col1.metric("Total Waste", f"{total_waste/1e6:.2f} M Tons")
col2.metric("Economic Loss", f"${economic_loss:,.0f} M")
col3.metric("Avg Waste / Capita", f"{avg_per_capita:.1f} Kg")
col4.metric("Household Waste %", f"{avg_household:.1f}%")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Country Analysis",
    "📦 Category Analysis",
    "📈 Trends",
    "💡 Insights"
])

# ---------------- COUNTRY ANALYSIS ----------------
with tab1:
    st.subheader("Food Waste by Country")

    fig = px.bar(
        filtered_df.groupby("Country", as_index=False)["Total Waste (Tons)"].sum(),
        x="Country",
        y="Total Waste (Tons)",
        title="Total Food Waste by Country",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CATEGORY ANALYSIS ----------------
with tab2:
    st.subheader("Economic Loss by Food Category")

    fig = px.pie(
        filtered_df.groupby("Food Category", as_index=False)["Economic Loss (Million $)"].sum(),
        names="Food Category",
        values="Economic Loss (Million $)",
        title="Economic Loss Contribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TREND ANALYSIS ----------------
with tab3:
    st.subheader("Yearly Waste Trend")

    trend_df = (
        filtered_df.groupby("Year", as_index=False)["Total Waste (Tons)"].sum()
    )

    fig = px.line(
        trend_df,
        x="Year",
        y="Total Waste (Tons)",
        markers=True,
        title="Total Food Waste Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
with tab4:
    st.subheader("Actionable Insights")

    top_country = (
        filtered_df.groupby("Country")["Total Waste (Tons)"].sum().idxmax()
        if not filtered_df.empty else "N/A"
    )

    top_category = (
        filtered_df.groupby("Food Category")["Economic Loss (Million $)"].sum().idxmax()
        if not filtered_df.empty else "N/A"
    )

    st.markdown(f"""
    **Key Findings**
    - **{top_country}** generates the highest total food waste  
    - **{top_category}** causes the highest economic loss  
    - Household waste contributes **~{avg_household:.1f}%** of total waste  
    - Monthly waste estimates indicate consistent, non-seasonal losses  

    **Policy Recommendations**
    - Target household-level awareness programs  
    - Subsidize cold storage for high-loss categories  
    - Incentivize redistribution of edible surplus  
    - Monitor per-capita waste, not just total waste  
    """)

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df)
