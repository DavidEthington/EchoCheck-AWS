import streamlit as st
import pandas as pd
from dispatcher import run_bulk_nxc

st.set_page_config(page_title="EchoCheck-nxc", layout="wide")
st.title("📡 EchoCheck: Cloud Credential Sprayer")

# Sidebar for Input (The "nxc -u" equivalent)
raw_input = st.sidebar.text_area("Paste Keys (Format: KEY:SECRET)", height=200)

if st.sidebar.button("🚀 Spray Credentials"):
    # Parse the input
    secrets = []
    for line in raw_input.split('\n'):
        if ":" in line:
            k, s = line.split(":", 1)
            secrets.append({"key": k.strip(), "secret": s.strip()})

    if secrets:
        with st.spinner(f"Spraying {len(secrets)} credentials..."):
            data = run_bulk_nxc(secrets)
            df = pd.DataFrame(data)

            # The Visual "Pwn" Representation
            def highlight_pwn(val):
                if val == "Pwned": return 'background-color: #ff4b4b; color: white'
                if val == "Active": return 'background-color: #ffa500'
                return ''

            st.table(df.style.applymap(highlight_pwn, subset=['s3_access']))
