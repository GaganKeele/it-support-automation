

detect_priority_prompt = """
You are an IT support classifier. Read this ticket description and classify its priority.

Description: "{description}"

Rules:
- high   = urgent, system down, cannot work at all, security issue
- medium = something broken but can partially work
- low    = minor issue, cosmetic, general question

Reply in EXACTLY this format and nothing else:
priority: <high/medium/low>
confidence: <number between 0 and 100>

Example reply:
priority: high
confidence: 92
"""

detect_issue_type_prompt = """
You are an IT support classifier. Read this ticket description and classify its issue type.

Description: "{description}"

Categories:
- wifi     = internet, network, connection, router issues
- login    = password, authentication, account access issues
- software = app crash, installation, program not working
- hardware = physical device, screen, keyboard, printer issues
- other    = anything that doesn't fit above

Reply in EXACTLY this format and nothing else:
issue_type: <wifi/login/software/hardware/other>
confidence: <number between 0 and 100>

Example reply:
issue_type: hardware
confidence: 85
"""

summary_decriptioin_prompt="""
You are an IT support assistant. Summarize this ticket in ONE sentence (max 15 words).
Description: "{description}"

Reply with ONLY the summary. No labels, no extra text.

"""