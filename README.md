# EchoCheck-AWS
EchoCheck AWS
Automated Credential Validation & Exposure Dashboard

EchoCheck is a lightweight, offensive-focused utility designed to identify, validate, and visualize exposed AWS credentials. Unlike standard scanners that merely flag strings, EchoCheck performs "quiet" STS validation to determine the real-world risk and permissions associated with discovered secrets.

Core Features
Multi-Format Ingestion: Supports .json, .csv, and .env files.

Active Validation: Uses boto3 to check the "heartbeat" of credentials via get-caller-identity.

Risk Quantification: Extracts Account IDs, ARNs, and basic permission levels.

Visual Dashboard: Streamlit-powered UI for real-time audit review.

USE THIS TOOL ONLY IN AN ETHICAL AND RESPONSIBLE MANNER

1. Clone the Repository & Navigate:

Bash
git clone https://github.com/DavidEthington/EchoCheck-AWS.git
cd EchoCheck-AWS

2. Set Up a Virtual Environment (Recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies:

Bash
pip install -r requirements.txt

4. Launch the Dashboard:

Bash
streamlit run app.py
Note: Once the command runs, your browser will automatically open to http://localhost:8501, where you can begin "spraying" your credentials.
