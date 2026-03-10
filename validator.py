import re

VALID_PRIORITIES = ['high', 'medium', 'low']
VALID_ISSUE_TYPES = ['wifi', 'login', 'software', 'hardware', 'other']

def validate_email(email):
    """Check if email has valid format like name@domain.com"""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email.strip()))

def validate_priority(priority):
    """Check if priority is High, Medium, or Low only"""
    if not priority or not isinstance(priority, str):
        return False
    return priority.strip().lower() in VALID_PRIORITIES

def validate_issue_type(issue_type):
    """Check if issue type is one of the known types"""
    if not issue_type or not isinstance(issue_type, str):
        return False
    return issue_type.strip().lower() in VALID_ISSUE_TYPES