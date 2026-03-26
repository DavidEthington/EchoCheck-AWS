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
