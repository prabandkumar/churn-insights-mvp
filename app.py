import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Churn Insights Dashboard", layout="wide")
today = pd.Timestamp(datetime.today().date())

st.title("📉 Churn Insights Dashboard")
st.caption("See why customers leave — and what to fix first.")


# EXPECTED DATA FORMAT

with st.expander("📄 Expected Data Format", expanded=False):
    st.markdown("""
| Column | Meaning |
|------|--------|
| customer_id | Unique customer |
| signup_date | Signup date (YYYY-MM-DD) |
| churn_date | Churn date or empty |
| is_churned | True / False |
| monthly_revenue | Monthly revenue |
- All insights use **only time & revenue**
""")

# SAMPLE CSV

st.download_button(
    "📥 Download sample CSV",
    data="""customer_id,signup_date,churn_date,is_churned,monthly_revenue
1,2023-01-01,2023-01-15,True,29
2,2023-01-05,,False,79
3,2023-01-10,2023-02-20,True,49
""",
    file_name="sample_churn.csv",
    mime="text/csv"
)

st.divider()


# USER ACTION

file = st.file_uploader("📤 Upload your CSV", type="csv")
use_sample = st.button("📊 View sample insights")

DATA_PATH = "universal_churn_sample_2200.csv"

if file:
    df = pd.read_csv(file)
elif use_sample:
    df = pd.read_csv(DATA_PATH)
else:
    st.info("Upload a CSV or view sample insights.")
    st.stop()


# VALIDATION

required = {"customer_id", "signup_date", "churn_date", "is_churned", "monthly_revenue"}
if not required.issubset(df.columns):
    st.error("CSV does not match expected format.")
    st.stop()


# CLEANING

df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["churn_date"] = pd.to_datetime(df["churn_date"], errors="coerce")
df["monthly_revenue"] = pd.to_numeric(df["monthly_revenue"], errors="coerce")
df = df.dropna(subset=["signup_date", "monthly_revenue"])

df["end_date"] = df["churn_date"].fillna(today)
df["days_active"] = (df["end_date"] - df["signup_date"]).dt.days

churned = df[df["is_churned"] == True]


# CORE INSIGHT

st.subheader("🧠 What’s happening")

early_churn_pct = (
    churned[churned["days_active"] <= 30].shape[0] /
    churned.shape[0] * 100
) if len(churned) else 0

lost_mrr = churned["monthly_revenue"].sum()

st.markdown(f"""
• **{early_churn_pct:.0f}%** of churn happens in the first 30 days  
• **${lost_mrr:,.0f}** in monthly revenue lost  
""")


# WHAT TO FIX

st.subheader("🎯 What to fix first")

if early_churn_pct > 50:
    st.error("""
**Customers leave before they understand the product.**

Fix onboarding:
- Shorten setup
- Guide users to first success fast
""")
else:
    st.warning("""
**Customers understand the product, but stop using it later.**

Fix retention:
- Remind users why the product matters
- Create repeat usage
""")
