import pandas as pd
from validator import validate_email, validate_priority, validate_issue_type
from transformer import normalize_fields, fix_ticket_ids, deduplicate_tickets
from router import assign_team, calculate_sla
from reporter import save_processed, save_rejected, save_summary
from ai_agent import detect_priority, detect_issue_type, summarize_description
from hitl import needs_human_review, human_review_issue, human_review_priority

def main():
    print("=" * 55)
    print("   AI-Powered IT Support Ticket Automation")
    print("     with Confidence Scoring + HITL Review")
    print("=" * 55)

    # ── STEP 1: Read Input ──────────────────────────────────
    try:
        df = pd.read_csv('input/ticket.csv')
        print(f"\n Loaded {len(df)} tickets from input/ticket.csv")
    except FileNotFoundError:
        print(" ERROR: input/ticket.csv not found!")
        return
    except Exception as e:
        print(f" ERROR reading file: {e}")
        return

    # ── STEP 2: Normalize Text ──────────────────────────────
    df = normalize_fields(df)

    # ── STEP 3: Fix Ticket IDs ──────────────────────────────
    df = fix_ticket_ids(df)

    # ── STEP 4: Validate + AI Fix + HITL ───────────────────
    processed_rows = []
    rejected_rows  = []

    for i, row in df.iterrows():
        reject_reason = None
        row['ai_fixed']      = ''
        row['ai_confidence'] = ''
        row['ai_summary']    = ''

        # ── Email: cannot be fixed by AI ──
        if not validate_email(str(row['email'])):
            reject_reason = 'Invalid email format'

        # ── Priority: AI fixes if invalid ──
        elif not validate_priority(str(row['priority'])):
            print(f"\ AI detecting priority for ticket {row['ticket_id']}...")
            ai_priority, confidence = detect_priority(str(row['description']))
            print(f"   Result → '{ai_priority}' (Confidence: {confidence}%)")

            # HITL: Ask human if confidence too low
            if needs_human_review(confidence):
                ai_priority = human_review_priority(
                    row['ticket_id'],
                    row['description'],
                    ai_priority,
                    confidence
                )
                row['ai_fixed']      = 'priority(human-reviewed)'
                row['ai_confidence'] = f"{confidence}% → human confirmed"
            else:
                row['ai_fixed']      = 'priority(ai-auto)'
                row['ai_confidence'] = f"{confidence}%"

            row['priority'] = ai_priority

        # ── Issue Type: AI fixes if unknown ──
        if reject_reason is None and not validate_issue_type(str(row['issue_type'])):
            print(f"\ AI detecting issue type for ticket {row['ticket_id']}...")
            ai_issue, confidence = detect_issue_type(str(row['description']))
            print(f"   Result → '{ai_issue}' (Confidence: {confidence}%)")

            # HITL: Ask human if confidence too low
            if needs_human_review(confidence):
                ai_issue = human_review_issue(
                    row['ticket_id'],
                    row['description'],
                    ai_issue,
                    confidence
                )
                row['ai_fixed']      += ' issue_type(human-reviewed)'
                row['ai_confidence'] += f" | issue:{confidence}% → human confirmed"
            else:
                row['ai_fixed']      += ' issue_type(ai-auto)'
                row['ai_confidence'] += f" | issue:{confidence}%"

            row['issue_type'] = ai_issue

        # ── Summarize description ──
        if reject_reason is None:
            print(f" Summarizing ticket {row['ticket_id']}...")
            row['ai_summary'] = summarize_description(str(row['description']))
            print(f"   Summary → {row['ai_summary']}")

        # ── Sort into processed or rejected ──
        if reject_reason:
            row['reject_reason'] = reject_reason
            rejected_rows.append(row)
        else:
            processed_rows.append(row)

    valid_df   = pd.DataFrame(processed_rows)
    invalid_df = pd.DataFrame(rejected_rows)

    print(f"\n After Validation + AI Fix:")
    print(f"   Valid   : {len(valid_df)}")
    print(f"   Invalid : {len(invalid_df)}")

    # ── STEP 5: Deduplicate ─────────────────────────────────
    if not valid_df.empty:
        keep_idx, reject_idx, reasons = deduplicate_tickets(valid_df)
        dup_df = valid_df.iloc[reject_idx].copy()
        dup_df['reject_reason'] = [reasons[i] for i in reject_idx]
        invalid_df = pd.concat([invalid_df, dup_df], ignore_index=True)
        valid_df   = valid_df.iloc[keep_idx].copy().reset_index(drop=True)

    # ── STEP 6: Route + SLA ─────────────────────────────────
    if not valid_df.empty:
        valid_df['assigned_team'] = valid_df['issue_type'].apply(assign_team)
        valid_df['sla_deadline']  = valid_df.apply(
            lambda r: calculate_sla(r['timestamp'], r['priority']), axis=1
        )

    # ── STEP 7: Save All Outputs ────────────────────────────
    save_processed(valid_df)
    save_rejected(invalid_df)
    save_summary(valid_df, invalid_df)

    # ── STEP 8: Final Summary ───────────────────────────────
    print("\n" + "=" * 55)
    print("  AUTOMATION COMPLETE")
    print("=" * 55)
    print(f"  Total Received  : {len(df)}")
    print(f"  Processed       : {len(valid_df)}")
    print(f"  Rejected        : {len(invalid_df)}")

    if not valid_df.empty:
        ai_auto   = valid_df['ai_fixed'].str.contains('ai-auto').sum()
        ai_human  = valid_df['ai_fixed'].str.contains('human-reviewed').sum()
        print(f"\n   AI Auto-Fixed    : {ai_auto} tickets")
        print(f"   Human Reviewed   : {ai_human} tickets")
        print(f"\n   Tickets Per Team:")
        for team, count in valid_df['assigned_team'].value_counts().items():
            print(f"     {team:<20}: {count}")
    print("=" * 55)

if __name__ == "__main__":
    main()
