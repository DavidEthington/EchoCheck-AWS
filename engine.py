import boto3
from datetime import datetime

class EchoCheckEngine:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def validate_and_enrich(self):
        """The main execution flow for a single secret."""
        # 1. Initial Ping (Validation)
        identity = self._check_identity()
        if not identity:
            return {"status": "Inactive", "risk": "None"}

        # 2. Get the 'Last Used' and 'Created' (Enrichment)
        metadata = self._get_iam_metadata(identity['Arn'])
        
        # 3. Combine it all for the Dashboard
        return {
            "status": "Active",
            "arn": identity['Arn'],
            "account_id": identity['Account'],
            "user": metadata['UserName'],
            "created_at": metadata['Created'],
            "last_used": metadata['LastUsed'],
            "region": metadata['Region'],
            "risk_level": self._calculate_risk(metadata['LastUsed'])
        }

    def _check_identity(self):
        """Quietly check if the key is valid."""
        try:
            sts = self.session.client('sts')
            return sts.get_caller_identity()
        except:
            return None

    def _get_iam_metadata(self, arn):
        """The metadata logic we discussed."""
        iam = self.session.client('iam')
        user_name = arn.split('/')[-1]
        
        # Pull Last Used
        last_used_resp = iam.get_access_key_last_used(AccessKeyId=self.access_key)
        usage = last_used_resp.get('AccessKeyLastUsed', {})
        
        # Pull Creation Date
        user_keys = iam.list_access_keys(UserName=user_name)
        created = next((k['CreateDate'] for k in user_keys['AccessKeyMetadata'] 
                       if k['AccessKeyId'] == self.access_key), "Unknown")
        
        return {
            "UserName": user_name,
            "LastUsed": usage.get('LastUsedDate', "Never"),
            "Region": usage.get('Region', "N/A"),
            "Created": created
        }

    def _calculate_risk(self, last_used):
        """Simple logic: If used recently, it's a higher priority."""
        if last_used == "Never":
            return "Medium (Stale Key)"
        # You could add logic here to check if it was used in the last 24 hours
        return "High (Active Leak)"
