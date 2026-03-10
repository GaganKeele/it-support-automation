# hitl.py — Human In The Loop
# Triggers when AI confidence is below threshold

CONFIDENCE_THRESHOLD = 60  # AI must be 60%+ sure, else ask human

ISSUE_OPTIONS = {
    '1': 'wifi',
    '2': 'login',
    '3': 'software',
    '4': 'hardware',
    '5': 'other'
}

PRIORITY_OPTIONS = {
    '1': 'high',
    '2': 'medium',
    '3': 'low'
}

def needs_human_review(confidence: int) -> bool:
    """Returns True if confidence is too low"""
    return confidence < CONFIDENCE_THRESHOLD


def human_review_issue(ticket_id: str, description: str,
                        ai_guess: str, confidence: int) -> str:
    """
    Ask human to confirm or correct AI's issue type guess.
    Returns: final issue type string
    """
    print("\n" + " " * 20)
    print("  HUMAN REVIEW NEEDED — LOW AI CONFIDENCE")
    print(" " * 20)
    print(f"\n  Ticket ID   : {ticket_id}")
    print(f"  Description : {description}")
    print(f"  AI Guessed  : {ai_guess}  (Confidence: {confidence}%)")
    print(f"\n  What is the correct issue type?")
    print(f"  1. wifi")
    print(f"  2. login")
    print(f"  3. software")
    print(f"  4. hardware")
    print(f"  5. other  ← (keep AI guess: '{ai_guess}')")
    print()

    while True:
        choice = input("  Your choice (1-5): ").strip()
        if choice in ISSUE_OPTIONS:
            selected = ISSUE_OPTIONS[choice]
            if choice == '5':
                print(f"  Keeping AI guess: '{ai_guess}'\n")
                return ai_guess
            else:
                print(f"  Human selected: '{selected}'\n")
                return selected
        else:
            print(" Invalid input. Please enter 1, 2, 3, 4, or 5.")


def human_review_priority(ticket_id: str, description: str,
                           ai_guess: str, confidence: int) -> str:
    """
    Ask human to confirm or correct AI's priority guess.
    Returns: final priority string
    """
    print("\n" + " " * 20)
    print("  HUMAN REVIEW NEEDED — LOW AI CONFIDENCE")
    print(" " * 20)
    print(f"\n  Ticket ID   : {ticket_id}")
    print(f"  Description : {description}")
    print(f"  AI Guessed  : {ai_guess}  (Confidence: {confidence}%)")
    print(f"\n  What is the correct priority?")
    print(f"  1. high")
    print(f"  2. medium")
    print(f"  3. low  ← (keep AI guess: '{ai_guess}')")
    print()

    while True:
        choice = input("  Your choice (1-3): ").strip()
        if choice in PRIORITY_OPTIONS:
            selected = PRIORITY_OPTIONS[choice]
            if choice == '3' and ai_guess == 'low':
                print(f"  Keeping AI guess: '{ai_guess}'\n")
                return ai_guess
            else:
                print(f"  Human selected: '{selected}'\n")
                return selected
        else:
            print(" Invalid input. Please enter 1, 2, or 3.")