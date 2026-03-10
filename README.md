# IT Support Ticket Automation
### Assessment 1 — AI Intern Practical Assessment

---

## Overview

This project automates the end-to-end processing of IT support tickets for a university environment. Support tickets arrive in a CSV file and are processed automatically — validated, cleaned, classified, routed to the correct team, and assigned SLA deadlines. Tickets with ambiguous or missing fields are handled intelligently using a locally running AI model instead of being blindly rejected.

The system is built entirely in Python and runs offline using Ollama with the llama3.2:3b model. No paid APIs or cloud services are used.

---

## Project Structure

```
IT_Support_Automation/
│
├── input/
│   └── tickets.csv              # Raw input data (messy, real-world format)
│
├── output/
│   ├── processed_tickets.csv    # Cleaned, valid tickets with team and SLA
│   ├── rejected_tickets.csv     # Invalid tickets with rejection reason
│   └── summary_report.xlsx      # Excel summary report
│
├── main.py                      # Entry point — runs the full pipeline
├── validator.py                 # Email and priority validation
├── transformer.py               # Text normalization, deduplication, ID generation
├── router.py                    # Team routing and SLA deadline calculation
├── reporter.py                  # Output file generation
├── ai_agent.py                  # AI classification and summarization (Ollama)
├── hitl.py                      # Human-in-the-Loop review for low-confidence decisions
└── README.md                    # This file
```

---

## Requirements

### System Requirements
- Python 3.9 or higher
- Ollama installed and running locally
- 8GB RAM minimum (16GB recommended)

### Install Ollama

**Windows:** Download from https://ollama.com/download and run the installer.

### Download the AI Model
ollama pull llama3.2:3b

### Install Python Dependencies
pip install pandas openpyxl ollama

---

## How to Run

# Step 1 — Navigate to the project folder
cd IT_Support_Automation

# Step 2 — Make sure Ollama is running
ollama serve

# Step 3 — Run the automation
python main.py

Output files will be saved automatically to the `output/` folder.

---

## Input Format

Place your ticket data in `input/tickets.csv`. The script handles messy, real-world data including missing values, invalid fields, and duplicates.

Required columns:

| Column | Description | Example |
|---|---|---|
| ticket_id | Unique identifier (can be missing or duplicate) | T001 |
| name | Submitter name | John Smith |
| email | Submitter email address | john@uni.edu |
| issue_type | Category of issue | wifi, login, software, hardware, other |
| priority | Urgency level | High, Medium, Low |
| description | Free-text description of the problem | Cannot connect to campus wifi |
| timestamp | When the ticket was submitted | 2026-03-10 09:00:00 |

---

## Automation Pipeline

The script processes every ticket through the following stages in order:

**Stage 1 — Load**
Reads the CSV file and reports the total number of tickets received.

**Stage 2 — Normalize**
Strips extra whitespace and converts text fields to lowercase for consistency.

**Stage 3 — Fix IDs**
Any ticket with a missing or duplicate ticket_id is automatically assigned a new unique ID using UUID generation.

**Stage 4 — Validate and AI-Fix**

- Email is checked against a standard format pattern. Tickets with invalid emails are rejected — this cannot be corrected automatically.
- Priority is checked. If the value is missing or invalid (for example "URGENT"), the AI reads the description and assigns the correct priority with a confidence score.
- Issue type is checked. If the value is unknown or unrecognized, the AI reads the description and assigns the correct category with a confidence score.
- If AI confidence is below 60%, the system pauses and asks the human operator to confirm or correct the decision (HITL review).
- Valid ticket descriptions are summarized into a single clean sentence by the AI.

**Stage 5 — Deduplicate**
Tickets from the same email address reporting the same issue type within a 24-hour window are identified as duplicates. Only the first submission is kept. Subsequent duplicates are moved to the rejected list with a clear reason.

**Stage 6 — Route and SLA**
Each valid ticket is assigned to the correct team and given an SLA deadline based on priority.

**Stage 7 — Output**
Three files are saved to the `output/` folder.

---

## Routing Rules

| Issue Type | Assigned Team |
|---|---|
| wifi | Network |
| login | IT Support |
| software | Applications |
| hardware | Infrastructure |
| other | General |

---

## SLA Rules

| Priority | Deadline |
|---|---|
| High | 4 hours from submission |
| Medium | 24 hours from submission |
| Low | 72 hours from submission |

---

## Output Files

**processed_tickets.csv**
Contains all valid, cleaned tickets. Includes the assigned team, SLA deadline, AI-generated summary, confidence score, and a flag indicating whether any field was fixed by AI or confirmed by a human.

**rejected_tickets.csv**
Contains tickets that could not be processed, with a reason for rejection. Common reasons include invalid email format and duplicate submission within 24 hours.

**summary_report.xlsx**
An Excel workbook with two sheets. The first sheet shows total tickets received, processed, and rejected. The second sheet shows a breakdown of tickets per assigned team.

---

## AI Features

### Local AI Model
The project uses llama3.2:3b running locally via Ollama. This means no data leaves the machine, there is no API cost, and the system works without an internet connection after the model is downloaded.

### Priority Detection
When a ticket has an invalid or missing priority, the AI reads the description and classifies it as high, medium, or low. It also returns a confidence score from 0 to 100.

### Issue Type Detection
When a ticket has an unknown issue type, the AI reads the description and classifies it into one of the five valid categories. It also returns a confidence score.

### Description Summarization
Every valid ticket has its description summarized into a single sentence of 15 words or fewer. This helps IT staff triage faster without reading long descriptions.

### Confidence Scoring
Every AI classification includes a confidence score. This prevents the system from blindly trusting AI decisions. The confidence score is saved to the output file for transparency.

---

## HITL — Human-in-the-Loop

When the AI confidence score for any classification falls below 60%, the automation pauses and presents the human operator with the ticket details and the AI's guess. The operator can confirm the AI's suggestion or select the correct value manually.

This is a deliberate design choice. In real IT environments, routing a ticket to the wrong team wastes engineer time and causes SLA breaches. HITL ensures that ambiguous tickets are handled correctly rather than silently misclassified.

The output file records whether each AI decision was auto-approved or human-reviewed, creating a full audit trail.

---

## Design Decisions

**Why Ollama and llama3.2:3b?**
It runs on consumer hardware (8-16GB RAM), requires no API key, costs nothing, and keeps all ticket data private on the local machine. The 3b model is fast enough for interactive HITL without frustrating delays.

**Why separate files instead of one large script?**
Each file has a single responsibility. This makes the code easier to test, debug, and extend. For example, swapping out the AI model only requires changes to ai_agent.py.

**Why deduplicate by email and issue type within 24 hours?**
This mirrors how real helpdesk systems work. A user who submits the same complaint twice in one day has not created a new problem — they are following up on an existing one. Keeping both creates duplicate work for IT staff.

**Why 60% as the HITL threshold?**
Below 60% confidence, the AI is essentially guessing. Automating a guess in a ticket routing system causes more harm than briefly asking a human. Above 60%, the AI is making a reasonably informed decision and can be trusted to act automatically.

---
