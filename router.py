from datetime import timedelta

ROUTING_MAP = {
    'wifi':     'Network',
    'login':    'IT Support',
    'software': 'Applications',
    'hardware': 'Infrastructure',
    'other':    'General'
}

SLA_HOURS = {
    'high':   4,
    'medium': 24,
    'low':    72
}

def assign_team(issue_type):
    """Return team name based on issue type"""
    return ROUTING_MAP.get(issue_type, 'General')

def calculate_sla(timestamp, priority):
    """Add SLA hours to timestamp to get deadline"""
    hours = SLA_HOURS.get(priority, 72)
    return timestamp + timedelta(hours=hours)