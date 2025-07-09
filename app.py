import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="HealthTrack Pro", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4fc3f7;'>🩺 HealthTrack Pro Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Load data
if os.path.exists("your_patient_data.csv"):
    df = pd.read_csv("your_patient_data.csv")
else:
    df = pd.DataFrame(columns=["Name", "Age", "Ward", "Status", "Checkup Date"])

# Data entry form
with st.form("patient_form"):
    st.subheader("➕ Add New Patient Record")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    ward = st.selectbox("Ward", ["Ward A", "Ward B", "Ward C"])
    status = st.selectbox("Status", ["Stable", "Critical", "Recovering"])
    date = st.date_input("Checkup Date")
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_data = {
            "Name": name,
            "Age": age,
            "Ward": ward,
            "Status": status,
            "Checkup Date": date
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("your_patient_data.csv", index=False)
        st.success("✅ Patient data added!")

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("👨‍⚕️ Total Patients", len(df))
col2.metric("🏥 Wards", df["Ward"].nunique())
col3.metric("🚨 Critical Cases", df[df["Status"] == "Critical"].shape[0])

# Charts
st.subheader("🏥 Ward Distribution")
ward_chart = px.histogram(df, x="Ward", color="Ward", title="Ward Distribution")
st.plotly_chart(ward_chart, use_container_width=True)

st.subheader("📊 Patient Status Breakdown")
status_chart = px.histogram(df, x="Status", color="Status", title="Status Breakdown")
st.plotly_chart(status_chart, use_container_width=True)

# Table
st.subheader("📋 Patient Table")
st.dataframe(df)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by Lisha Ghosh</p>", unsafe_allow_html=True)
