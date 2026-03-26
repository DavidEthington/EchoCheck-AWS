import boto3
from botocore.exceptions import ClientError

def audit_iam(session):
    iam = session.client('iam')
    pwn_score = 0
    findings = []
    
    # List of "High-Impact" actions to check
    # We try a "Dry Run" by just attempting to list things first
    try:
        # 1. Can we see other users? (Recon)
        users = iam.list_users(MaxItems=5)['Users']
        findings.append(f"ListUsers: Success ({len(users)} found)")
        pwn_score += 1
        
        # 2. Can we see policies? (Path to PrivEsc)
        policies = iam.list_policies(Scope='Local', MaxItems=5)['Policies']
        findings.append(f"ListPolicies: Success")
        pwn_score += 1
        
        # 3. Check for the "Holy Grail": Can we create an Access Key?
        # We don't actually do it, we just check if we can list them for ourselves
        user_identity = session.client('sts').get_caller_identity()
        user_name = user_identity['Arn'].split('/')[-1]
        iam.list_access_keys(UserName=user_name)
        findings.append("ListOwnKeys: Success")
        
    except ClientError as e:
        findings.append(f"Access Limited: {e.response['Error']['Code']}")

    # Determine Status
    status = "Active"
    if pwn_score >= 2:
        status = "Pwned (Admin/PowerUser)"
    elif pwn_score == 1:
        status = "Read-Only (IAM)"

    return {
        "status": status,
        "summary": " | ".join(findings),
        "can_escalate": pwn_score >= 2
    }
