import streamlit as st
import pandas as pd
from dispatcher import run_bulk_nxc

# --- Page Configuration ---
st.set_page_config(
    page_title="EchoCheck-AWS",
    page_icon="📡",
    layout="wide"
)

st.title("📡 EchoCheck: Cloud Credential Sprayer")
st.markdown("""
    **NetExec-style** assessment for AWS IAM credentials. 
    Paste your keys in the sidebar to begin the multi-threaded service spray.
""")

# --- Sidebar Configuration ---
st.sidebar.header("Credential Input")
st.sidebar.info("Format: `ACCESS_KEY:SECRET_KEY` (one per line)")

raw_input = st.sidebar.text_area("Paste Keys here:", height=300)
thread_count = st.sidebar.slider("Concurrent Threads", 1, 50, 10)

# --- Action Trigger ---
if st.sidebar.button("🚀 Spray Credentials"):
    if not raw_input.strip():
        st.sidebar.error("Please provide at least one credential pair.")
    else:
        # 1. Parse Input
        secrets = []
        for line in raw_input.split('\n'):
            if ":" in line:
                try:
                    k, s = line.split(":", 1)
                    secrets.append({"key": k.strip(), "secret": s.strip()})
                except ValueError:
                    continue

        if not secrets:
            st.error("No valid credentials found. Ensure format is KEY:SECRET")
        else:
            with st.spinner(f"Spraying {len(secrets)} credentials across {thread_count} threads..."):
                # 2. Execute Dispatcher
                results = run_bulk_nxc(secrets)
                df = pd.DataFrame(results)

                # 3. Defensive UI Logic
                if df.empty:
                    st.warning("Scan completed, but no data was returned.")
                else:
                    # Clean up column names (ensures consistency with our styling)
                    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

                    # Define the "Pwned" Heatmap styling
                    def highlight_pwn(val):
                        if isinstance(val, str):
                            if "Pwned" in val:
                                return 'background-color: #9e1a1a; color: white; font-weight: bold'
                            if "Active" in val or "Success" in val:
                                return 'background-color: #1e5c2d; color: white'
                        return ''

                    # Identify styling targets safely
                    style_targets = [c for c in ['s3_access', 'iam_access', 'status'] if c in df.columns]

                    st.subheader("Results Matrix")
                    # Display the styled dataframe
                    st.dataframe(
                        df.style.applymap(highlight_pwn, subset=style_targets),
                        use_container_width=True
                    )
                    
                    st.success(f"Scan Complete. {len(df)} credentials processed.")

# --- Footer ---
st.divider()
st.caption("EchoCheck-AWS | Principal Security Engineering Framework")
