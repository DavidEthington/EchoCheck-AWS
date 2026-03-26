import boto3
from botocore.exceptions import ClientError

def validate_aws_key(access_key, secret_key):
    try:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        
        # If we get here, the key is valid. 
        # Now let's see what it can actually do (simplified check)
        iam = session.client('iam')
        user_name = identity['Arn'].split('/')[-1]
        
        return {
            "status": "Active",
            "account": identity['Account'],
            "arn": identity['Arn'],
            "user": user_name
        }
    except ClientError as e:
        return {"status": "Inactive/Invalid", "error": str(e)}
