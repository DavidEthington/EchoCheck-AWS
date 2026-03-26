import boto3

def audit_s3(session):
    try:
        s = session.client('s3')
        buckets = s.list_buckets()['Buckets']
        count = len(buckets)
        return {
            "status": "Pwned" if count > 0 else "Active",
            "summary": f"Found {count} buckets.",
            "metadata": {"buckets": [b['Name'] for b in buckets[:5]]}
        }
    except:
        return {"status": "Denied", "summary": "No S3 Access."}
