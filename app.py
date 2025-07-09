import streamlit as st
import pandas as pd
import os

st.set_page_config("HealthTrack Pro", layout="wide")
st.title("🩺 HealthTrack Pro: Live Patient Monitoring")

# --- CSV File ---
DATA_FILE = "patients.csv"

# --- Load or Create CSV ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Name", "Age", "Ward", "Status", "CheckupDate", "HeartRate"])
    df.to_csv(DATA_FILE, index=False)

# --- Input Form ---
with st.form("patient_form"):
    st.subheader("📥 Add New Patient Data")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 150)
    ward = st.selectbox("Ward", ["Ward A", "Ward B", "Ward C"])
    status = st.selectbox("Status", ["Stable", "Critical", "Recovered"])
    date = st.date_input("Checkup Date")
    hr = st.number_input("Heart Rate", 30, 200)
    
    submitted = st.form_submit_button("Add Patient")
    
    if submitted:
        new_data = {
            "Name": name, "Age": age, "Ward": ward,
            "Status": status, "CheckupDate": date, "HeartRate": hr
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Patient data added successfully.")

# --- Display Dashboard ---
st.subheader("📊 Live Dashboard")

# Pie Chart - Ward Distribution
ward_counts = df["Ward"].value_counts()
st.write("**Ward Distribution**")
st.bar_chart(ward_counts)

# Bar Chart - Status Count
status_counts = df["Status"].value_counts()
st.write("**Status Breakdown**")
st.bar_chart(status_counts)

# Line Chart - Heart Rate over Time
df["CheckupDate"] = pd.to_datetime(df["CheckupDate"])
hr_chart = df.groupby("CheckupDate")["HeartRate"].mean()
st.write("**Heart Rate Over Time**")
st.line_chart(hr_chart)

# Table - All Data
st.write("**All Patient Records**")
st.dataframe(df)
