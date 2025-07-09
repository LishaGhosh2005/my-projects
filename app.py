import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load patient data
DATA_FILE = "your_patient_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="HealthTrack Pro", layout="wide")
st.title("🩺 HealthTrack Pro: Live Patient Monitoring")

# Load data
df = load_data()

# Sidebar – Add new patient
st.sidebar.header("➕ Add New Patient")
with st.sidebar.form("new_patient_form"):
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    ward = st.selectbox("Ward", ["A", "B", "C", "ICU", "ER"])
    status = st.selectbox("Health Status", ["Stable", "Critical", "Recovering"])
    checkup_date = st.date_input("Checkup Date", value=datetime.today())
    submitted = st.form_submit_button("Add Patient")

    if submitted:
        new_data = {
            "Name": name,
            "Age": age,
            "Ward": ward,
            "Status": status,
            "Checkup Date": checkup_date.strftime("%Y-%m-%d")
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        st.success(f"Patient '{name}' added successfully!")

# Dashboard section
st.subheader("📊 Patient Summary Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("👨‍⚕️ Total Patients", len(df))
col2.metric("🛏️ Wards Covered", df['Ward'].nunique())
col3.metric("📅 Last Checkup", df['Checkup Date'].max())

# Chart 1: Patient count by ward
fig1 = px.bar(df.groupby('Ward').size().reset_index(name='Count'),
              x='Ward', y='Count', title="Patients by Ward")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Patient count by status
fig2 = px.pie(df, names='Status', title="Patient Health Status Distribution")
st.plotly_chart(fig2, use_container_width=True)

# View raw data
with st.expander("🗂️ View Patient Records"):
    st.dataframe(df)

