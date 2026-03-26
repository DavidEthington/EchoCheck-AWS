import boto3
import concurrent.futures
from modules.s3 import audit_s3

class EchoCheckDispatcher:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def validate_and_spray(self):
        """Validates the key, then runs all active plugins."""
        try:
            sts = self.session.client('sts')
            identity = sts.get_caller_identity()
        except:
            return {"status": "Dead", "key": self.access_key}

        # If alive, run the "Plugins" (S3, IAM, etc.)
        # In a real nxc tool, you'd loop through a 'modules' folder
        s3_results = audit_s3(self.session)
        
        return {
            "status": "Active",
            "account": identity['Account'],
            "arn": identity['Arn'],
            "s3_access": s3_results['status'],
            "s3_summary": s3_results['summary']
        }

def run_bulk_nxc(secrets_list):
    """The Multi-Threaded Sprayer."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(EchoCheckDispatcher(s['key'], s['secret']).validate_and_spray) for s in secrets_list]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
    return results
