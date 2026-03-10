import pandas as pd
import os

def save_processed(df, path='output/processed_tickets.csv'):
    os.makedirs('output', exist_ok=True)
    df.to_csv(path, index=False)
    print(f" Processed tickets saved → {path}")

def save_rejected(df, path='output/rejected_tickets.csv'):
    os.makedirs('output', exist_ok=True)
    df.to_csv(path, index=False)
    print(f" Rejected tickets saved → {path}")

def save_summary(processed_df, rejected_df, path='output/summary_report.xlsx'):
    os.makedirs('output', exist_ok=True)

    total = len(processed_df) + len(rejected_df)
    processed_count = len(processed_df)
    rejected_count = len(rejected_df)

    # Tickets per team
    if not processed_df.empty:
        per_team = processed_df.groupby('assigned_team').size().reset_index()
        per_team.columns = ['Team', 'Ticket Count']
    else:
        per_team = pd.DataFrame(columns=['Team', 'Ticket Count'])

    # Overview sheet data
    overview = pd.DataFrame({
        'Metric': ['Total Tickets Received', 'Processed', 'Rejected'],
        'Count':  [total, processed_count, rejected_count]
    })

    # Write to Excel with 2 sheets
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        overview.to_excel(writer, sheet_name='Summary', index=False)
        per_team.to_excel(writer, sheet_name='Tickets Per Team', index=False)

    print(f" Summary report saved → {path}")