import streamlit as st
import pandas as pd
from engine import EchoCheckEngine  # This imports the logic we just built
from loader import load_secrets      # This imports your JSON/ENV loader

st.set_page_config(page_title="EchoCheck AWS", layout="wide")

st.title("📡 EchoCheck AWS")
st.subheader("Credential Validation & Exposure Dashboard")

# 1. Sidebar for File Upload
uploaded_file = st.sidebar.file_uploader("Upload Secrets (JSON, CSV, ENV)", type=['json', 'csv', 'env'])

if uploaded_file:
    # Save temp file or process directly
    secrets_list = load_secrets(uploaded_file) 
    results = []

    st.info(f"Loaded {len(secrets_list)} potential secrets. Validating...")

    # 2. Run the Engine for each secret
    for secret in secrets_list:
        engine = EchoCheckEngine(secret['access_key'], secret['secret_key'])
        data = engine.validate_and_enrich()
        results.append(data)

    # 3. Display the Results in a Dataframe
    df = pd.DataFrame(results)
    
    # Color-coding the Status column
    def color_status(val):
        color = 'green' if val == 'Active' else 'red'
        return f'color: {color}'

    st.dataframe(df.style.applymap(color_status, subset=['status']))

    # 4. Summary Metrics
    active_count = len(df[df['status'] == 'Active'])
    st.sidebar.metric("Active Leaks Found", active_count, delta_color="inverse")
