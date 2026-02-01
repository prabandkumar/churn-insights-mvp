import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Churn Insights for Founders", layout="wide")

st.title("📉 Churn Insights Dashboard")
st.write("Upload customer data and instantly understand churn.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Clean
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)

    # Churn Rate
    churn_rate = (df["Churn"] == "Yes").mean() * 100
    st.metric("Overall Churn Rate", f"{churn_rate:.2f}%")

    # Churn by Tenure
    st.subheader("Churn by Customer Tenure")
    fig, ax = plt.subplots()
    df.groupby("tenure")["Churn"].apply(lambda x: (x == "Yes").mean()).plot(ax=ax)
    ax.set_ylabel("Churn Rate")
    st.pyplot(fig)

    # Risky Users
    st.subheader("High Risk Customers")
    risky = df[(df["tenure"] < 6) & (df["Churn"] == "Yes")]
    st.write(f"{len(risky)} customers churned within first 6 months")

    # Insights
    st.subheader("🔍 Key Insights")
    st.write("""
    • Customers who churn mostly leave within the first 6 months  
    • Early engagement is critical to retention  
    • Founders should focus onboarding efforts in the first 30 days  
    """)
else:
    st.info("Upload a CSV file to begin.")
