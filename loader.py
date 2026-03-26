import json
import pandas as pd # For CSV/Excel handling

def load_secrets(file_path):
    if file_path.endswith('.json'):
        with open(file_path) as f:
            return json.load(f)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path).to_dict('records')
    elif file_path.endswith('.env'):
        # Simple logic to parse KEY=VALUE pairs
        secrets = {}
        with open(file_path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    secrets[k] = v
        return [secrets]
