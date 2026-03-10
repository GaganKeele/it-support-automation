import ollama
from prompt import detect_priority_prompt, detect_issue_type_prompt, summary_decriptioin_prompt
MODEL = "llama3.2:3b"

def detect_priority(description: str) -> tuple[str, int]:
    """
    Detect priority from description.
    Returns: (priority, confidence_score)
    Example: ('high', 87)
    """
    prompt = detect_priority_prompt.format(description=description)
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return _parse_response(
            response['message']['content'],
            valid_values=['high', 'medium', 'low'],
            default='low'
        )
    except Exception as e:
        print(f"  AI priority detection failed: {e}")
        return ('low', 0)


def detect_issue_type(description: str) -> tuple[str, int]:
    """
    Detect issue type from description.
    Returns: (issue_type, confidence_score)
    Example: ('hardware', 78)
    """
    prompt = detect_issue_type_prompt.format(description=description)
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return _parse_response(
            response['message']['content'],
            valid_values=['wifi', 'login', 'software', 'hardware', 'other'],
            default='other'
        )
    except Exception as e:
        print(f"  AI issue detection failed: {e}")
        return ('other', 0)


def summarize_description(description: str) -> str:
    """
    Summarize ticket description into 1 clean sentence.
    Returns: summary string
    """

    prompt=summary_decriptioin_prompt.format(description=description)
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"  AI summarization failed: {e}")
        return description


def _parse_response(raw: str, valid_values: list, default: str) -> tuple[str, int]:
    """
    Internal helper — parses AI response like:
    'issue_type: hardware\\nconfidence: 85'
    Returns: ('hardware', 85)
    """
    value = default
    confidence = 50  # default confidence

    try:
        lines = raw.strip().lower().splitlines()
        for line in lines:
            # Parse value (priority or issue_type)
            if ':' in line:
                parts = line.split(':', 1)
                key = parts[0].strip()
                val = parts[1].strip()

                if key in ['priority', 'issue_type'] and val in valid_values:
                    value = val

                elif key == 'confidence':
                    try:
                        confidence = int(''.join(filter(str.isdigit, val)))
                        confidence = max(0, min(100, confidence))  # clamp 0-100
                    except:
                        confidence = 50
    except:
        pass

    return (value, confidence)

