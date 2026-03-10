# IT Support Ticket Automation
**Assessment 1 — AI Intern Practical Assessment**

---

## Overview

This project automates the end-to-end processing of IT support tickets for a university environment. Support tickets arrive in a CSV file and are processed automatically — validated, cleaned, classified, routed to the correct team, and assigned SLA deadlines.

Tickets with ambiguous or missing fields are handled intelligently using a locally running AI model instead of being blindly rejected. The system is built entirely in Python and runs offline using Ollama with the `llama3.2:3b` model. No paid APIs or cloud services are used.

---

## Project Structure

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

---

## Automation Flow

INPUT
tickets.csv
     |
     v
NORMALIZE TEXT
Strip spaces, lowercase
     |
     v
FIX TICKET IDs
Generate UUID if missing or duplicate
     |
     v
VALIDATE EMAIL --------FAIL---------> rejected_tickets.csv
     |
     v
VALID PRIORITY?
  |
  NO -----> AI detects priority + confidence score
                   |
                   |--- confidence >= 60% ---> Auto approved
                   |--- confidence  < 60% ---> HITL: Ask Human
     |
     v
VALID ISSUE TYPE?
  |
  NO -----> AI detects issue type + confidence score
                   |
                   |--- confidence >= 60% ---> Auto approved
                   |--- confidence  < 60% ---> HITL: Ask Human
     |
     v
AI SUMMARIZES DESCRIPTION (1 sentence)
     |
     v
DEDUPLICATE
Same email + issue within 24h? -----> rejected_tickets.csv
     |
     v
ASSIGN TEAM + CALCULATE SLA DEADLINE
     |
     v
OUTPUT
├── processed_tickets.csv
├── rejected_tickets.csv
└── summary_report.xlsx

---

## Requirements

- Python 3.9 or higher
- Ollama installed and running locally
- 8GB RAM minimum (16GB recommended)

---

## Setup Instructions

**Step 1 — Install Ollama**

Windows: Download and run the installer from https://ollama.com/download

Mac:
brew install ollama

Linux:
curl -fsSL https://ollama.com/install.sh | sh

**Step 2 — Download the AI Model**

ollama pull llama3.2:3b

**Step 3 — Install Python Dependencies**

pip install pandas openpyxl ollama

---

## How to Run

# Navigate to the project folder
cd IT_Support_Automation

# Start Ollama
ollama serve

# Run the automation
python main.py

Output files are saved automatically to the `output/` folder.

---

## Input Format

Place ticket data in `input/tickets.csv`. The script handles messy real-world data including missing values, invalid fields, and duplicates.

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

**processed_tickets.csv** — All valid cleaned tickets with assigned team, SLA deadline, AI summary, confidence score, and audit flag showing whether a field was auto-fixed or human-reviewed.

**rejected_tickets.csv** — Tickets that could not be processed, with a clear rejection reason for each.

**summary_report.xlsx** — Excel workbook with two sheets: overall totals (received, processed, rejected) and a per-team ticket breakdown.

---

## AI Features

### Local AI Model
Uses `llama3.2:3b` via Ollama — runs fully offline, no API key needed, no data leaves the machine.

### Priority Detection
When priority is missing or invalid (e.g. "URGENT"), the AI reads the ticket description and assigns `high`, `medium`, or `low` with a confidence score.

### Issue Type Detection
When issue type is unknown, the AI reads the description and classifies it into one of the five valid categories with a confidence score.

### Description Summarization
Every valid ticket description is summarized into a single sentence (15 words or fewer) to help IT staff triage faster.

### Confidence Scoring
Every AI decision includes a confidence score from 0 to 100. Scores are saved to the output file for full transparency.

---

## HITL — Human-in-the-Loop

When AI confidence falls below 60%, the automation pauses and shows the human operator the ticket details along with the AI guess. The operator can confirm or correct the decision before processing continues.

This prevents silent misclassification. In real IT environments, routing a ticket to the wrong team wastes engineer time and causes SLA breaches. Every HITL decision is recorded in the output file as an audit trail.

---

## Author

**Name:** Gagan Keele  
**Date:** March 2026  
**Assessment:** AI Intern Practical — Assessment 1