import uuid
import pandas as pd

def normalize_fields(df):
    """Strip spaces and lowercase text fields"""
    text_cols = ['name', 'email', 'issue_type', 'priority', 'description']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df['issue_type'] = df['issue_type'].str.lower()
    df['priority'] = df['priority'].str.lower()
    return df

def generate_unique_id():
    """Create a new unique ticket ID"""
    return 'T-' + str(uuid.uuid4())[:8].upper()

def fix_ticket_ids(df):
    """Fix missing or duplicate ticket IDs"""
    seen_ids = set()
    new_ids = []
    for tid in df['ticket_id']:
        tid_str = str(tid).strip()
        # Missing ID (empty, nan, None)
        if tid_str in ['', 'nan', 'None']:
            new_ids.append(generate_unique_id())
        # Duplicate ID
        elif tid_str in seen_ids:
            new_ids.append(generate_unique_id())
        else:
            seen_ids.add(tid_str)
            new_ids.append(tid_str)
    df['ticket_id'] = new_ids
    return df

def deduplicate_tickets(df):
    """
    Remove duplicate tickets:
    Same email + same issue_type within 24 hours = duplicate
    Keep first, reject rest
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.sort_values('timestamp').reset_index(drop=True)

    keep_indices = []
    reject_indices = []
    reject_reasons = {}

    seen = []  # list of (email, issue_type, timestamp)

    for i, row in df.iterrows():
        is_dup = False
        for (s_email, s_issue, s_time) in seen:
            same_email = row['email'] == s_email
            same_issue = row['issue_type'] == s_issue
            time_diff = abs((row['timestamp'] - s_time).total_seconds())
            within_24h = time_diff <= 86400  # 86400 seconds = 24 hours
            if same_email and same_issue and within_24h:
                is_dup = True
                break
        if is_dup:
            reject_indices.append(i)
            reject_reasons[i] = 'Duplicate ticket (same email+issue within 24h)'
        else:
            keep_indices.append(i)
            seen.append((row['email'], row['issue_type'], row['timestamp']))

    return keep_indices, reject_indices, reject_reasons