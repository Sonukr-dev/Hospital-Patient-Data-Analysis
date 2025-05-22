import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Page setup
st.set_page_config(page_title="🏥 Hospital Data Dashboard", layout="wide")
st.title("🏥 Hospital Patient Data Analysis")


# Upload CSV or use default
uploaded_file = st.sidebar.file_uploader("📤 Upload your hospital_data.csv", type="csv")

@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates=["Admission_Date", "Discharge_Date"])
    df["Length_of_Stay"] = (df["Discharge_Date"] - df["Admission_Date"]).dt.days
    return df


# Load data
if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("ℹ️ No file uploaded. Using default preview dataset `hospital_data.csv`.")
    default_path = "hospital_data.csv"
    if not os.path.exists(default_path):
        st.error("❌ Default dataset not found. Please upload a file.")
        st.stop()
    df = load_data(default_path)


# Display dataframe
st.subheader("📄 Data Preview")
st.dataframe(df.head())


# Basic Stats
st.subheader("📊 Summary Statistics")
st.write(df.describe(include='all'))


# Gender Distribution
st.subheader("👤 Gender Distribution")
gender_count = df["Gender"].value_counts()
st.bar_chart(gender_count)


# Department-wise patient count
st.subheader("🏥 Patients per Department")
dept_count = df["Department"].value_counts()
st.bar_chart(dept_count)


# Disease distribution
st.subheader("🦠 Common Diseases")
disease_count = df["Disease"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=disease_count.values, y=disease_count.index, ax=ax)
st.pyplot(fig)



# Outcome distribution
st.subheader("📈 Patient Outcomes")
outcome_count = df["Outcome"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(outcome_count, labels=outcome_count.index, autopct="%1.1f%%", startangle=140)
st.pyplot(fig2)


# Cost Analysis
st.subheader("💰 Treatment Cost Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(df["Cost"], kde=True, ax=ax3)
st.pyplot(fig3)


# Length of Stay
st.subheader("🛏️ Length of Stay")
fig4, ax4 = plt.subplots()
sns.boxplot(x="Department", y="Length_of_Stay", data=df, ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)



# Monthly Admissions
st.subheader("📅 Monthly Admissions")
df["Admission_Month"] = df["Admission_Date"].dt.to_period("M").astype(str)
monthly_admissions = df["Admission_Month"].value_counts().sort_index()
st.line_chart(monthly_admissions)



# Example filter
selected_departments = st.sidebar.multiselect("Filter by Department", df["Department"].unique(), default=df["Department"].unique())
df = df[df["Department"].isin(selected_departments)]


#Average Cost by Department/Disease
st.subheader("💵 Average Cost by Department")
avg_cost = df.groupby("Department")["Cost"].mean().sort_values(ascending=False)
st.bar_chart(avg_cost)


# Download button
st.subheader("📥 Download Filtered Data")
st.download_button("Download Filtered Data", df.to_csv(index=False), "filtered_data.csv")

