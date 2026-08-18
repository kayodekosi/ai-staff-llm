# Knatware AI Staff LLM

**LLM-powered staff personas, role-aware system prompts, and fine-tuning assets for the Knatware AI Workforce platform.**

This repository turns a full company organogram (97 staff members across 9 departments) into production-ready LLM artefacts: per-person system prompts, chat-format fine-tuning data, reporting-line context, and a clear migration path from CSV to a future database.

**Product of Knatware Technology UK**  
**Developed by Kayode Okosi, LLM Developer**

| Resource | Link |
|----------|------|
| Platform | [knatware.com/knat](https://knatware.com/knat) |
| LLM ops & PASTA | [github.com/kayodekosi/LLM](https://github.com/kayodekosi/LLM) |
| AI-Workforce (Java platform) | [github.com/kayodekosi/ai-workforce](https://github.com/kayodekosi/ai-workforce) |
| Developer | [github.com/kayodekosi](https://github.com/kayodekosi) |

---

## What this repository does

Knatware runs an **AI-staffed organisation**: many roles are filled by AI agents (and some by humans). Each agent needs:

1. A **stable identity** (name, title, department, contact details)
2. A **role brief** (what they are tasked with)
3. **Reporting-line awareness** (who they report to and when to escalate)
4. Optional **specialised fine-tuning** so the model stays in character

This repo is the bridge between the organogram and those LLM requirements.

### Inputs
- Full organogram CSV (`data/organogram.csv`) — 97 people, 9 departments  
- Each row includes a rich **Notes** field: a detailed “As the {title} in the {department}… you are tasked with…” role brief

### Outputs
- **97 individual system prompts** (`llm/prompts/generated/`) ready to inject into chat or agent runtimes  
- **Chat-format JSONL** for supervised fine-tuning / QLoRA (Unsloth Studio, PASTA methodology, Nemotron or similar small instruct models)  
- **Reporting-line map** so prompts know the organisational hierarchy  
- **Scripts** that regenerate everything from the CSV (or, later, from a database) without changing the LLM-facing contracts  
- Documentation for architecture, usage, schema, and the future DB migration

---

## Departments covered

| Department | Example roles |
|------------|----------------|
| Executive Office | AI CEO |
| Information Technology | IT Director, AI Development Lead, Software Developers, QA, Security, Network, Helpdesk, Systems Engineers |
| Crypto & Trading | AI Trading Lead, Algorithm Developer, Market Prediction, Portfolio Optimizer, Blockchain Analyst, Trade Bot |
| Finance & Administration | Finance Controller, Budget Analyst, Procurement, Project Coordinator, AI Secretary |
| Human Resources | AI HR Manager, Recruitment, Training, Employee Relations |
| Product Management | Product Manager, Feature Designer, UX Analyst, Go-to-Market, Customer Support |
| Research & Development | Research Lead, Algorithm Researcher, Model Architect, Prototype Developer, Innovation Specialist |
| Ethics & Compliance | Ethics Officer, Fairness Analyst, Transparency, Legal Advisor, Privacy Advocate |
| Strategic Advisory | Human Adviser, Market Researcher, Policy Analyst, Innovation Scout |

---

## Repository layout

```
knatware-ai-staff-llm/
├── README.md                          # This file
├── LICENSE                            # MIT
├── ATTRIBUTION.md                     # Knatware Technology UK / Kayode Okosi
├── data/
│   ├── organogram.csv                 # Full staff list (97 rows) with rich Notes
│   ├── schema.md                      # Column definitions
│   └── future-db-notes.md             # How this maps to a future database
├── llm/
│   ├── prompts/
│   │   ├── base_system_template.txt   # Template used by the generator
│   │   └── generated/                 # 97 ready-to-use system prompts
│   ├── datasets/
│   │   └── staff_role_sft_sample.jsonl  # Sample chat JSONL for fine-tuning
│   ├── pasta-fine-tune/
│   │   ├── hyperparameters.yaml       # QLoRA settings for Unsloth Studio
│   │   └── expected-loss-curve.md     # What a healthy training curve looks like
│   └── reporting-lines.md             # Inferred hierarchy until DB has reports_to
├── scripts/
│   ├── generate_role_prompts.py       # CSV → per-staff system prompts
│   └── csv_to_jsonl.py                # CSV → chat-format fine-tuning data
└── docs/
    ├── architecture.md                # Current vs future data flow
    ├── usage.md                       # Step-by-step usage
    └── GITHUB_DESCRIPTION.md          # Copy-paste GitHub About + topics
```

---

## Quick start

```bash
# 1. Generate (or regenerate) all 97 system prompts
python scripts/generate_role_prompts.py \
  --csv data/organogram.csv \
  --out llm/prompts/generated/

# 2. Build a fine-tuning dataset (example: first 40 staff, 4 turns each)
python scripts/csv_to_jsonl.py \
  --csv data/organogram.csv \
  --out llm/datasets/staff_role_sft.jsonl \
  --max 40
```

Load the JSONL into **Unsloth Studio** (or any SFT trainer). Use the hyperparameters in `llm/pasta-fine-tune/hyperparameters.yaml`. Recommended base model for low-VRAM experiments: **NVIDIA Nemotron 3 Nano 4B** (or a similar small instruct model) with QLoRA.

---

## How the prompts are built

Each generated system prompt contains:

1. **Identity** — Display name, job title, department  
2. **Contact** — Primary email and work phone / extension  
3. **Reporting line** — Inferred manager (department lead) until a real `reports_to` field exists in the database  
4. **Role brief** — The full text from the CSV `Notes` column (the detailed “you are tasked with…” description)  
5. **Behaviour rules** — Stay in character, escalate appropriately, do not invent policy, treat AI and human colleagues equally  

Example (abbreviated):

```text
You are Emma Chief, AI CEO in the Executive Office department at Knatware Technology UK.

Email: emma.chief@knatware.co.uk | Extension: 1001
Reports (organisational): — (top of organisation)

As the AI CEO in the Executive Office at Knatware Technology UK, you are tasked with defining the strategic vision for integrating AI technologies across all departments...

Stay strictly in character: ...
```

---

## Fine-tuning (PASTA / Unsloth)

This repo is designed to work with the **PASTA** methodology (Parameter-efficient Adaptation for Specialized Task Alignment) and Unsloth Studio:

- Method: **QLoRA** (4-bit base + LoRA adapters)  
- Typical settings: rank 16, alpha 32, LR 2e-4, 2 epochs, context 2048  
- Expected final train loss on small persona sets: roughly **0.9 – 1.4**  
- See `llm/pasta-fine-tune/` for exact YAML and loss-curve guidance  

You can fine-tune:

- One global “staff persona” adapter  
- Or department-level adapters (filter the CSV by Department before running `csv_to_jsonl.py`)

---

## Staff data and the future database

**Current source of truth:** `data/organogram.csv`

Staff data will eventually live in a database used by the AI-Workforce platform. Design principles:

1. Generators accept either a CSV path or (later) a DB connection — same output format.  
2. LLM contracts (system prompt shape, JSONL message format) **do not change**.  
3. Reporting lines will become a first-class `reports_to` field; until then the scripts use a lightweight department → lead map (see `llm/reporting-lines.md`).  
4. Seeding remains idempotent so re-import does not break existing chat history or adapter IDs.

See `data/future-db-notes.md` and `data/schema.md` for the suggested table shape and column mapping.

---

## Integration with AI-Workforce

The [AI-Workforce](https://github.com/kayodekosi/ai-workforce) Spring Boot platform already models staff, departments, chat channels and connectors. This repository supplies the **LLM layer** for those staff:

- Load a generated system prompt when an AI staff member joins a chat  
- Optionally route that staff member through a fine-tuned adapter  
- Keep identity and reporting structure consistent with the organogram (and later the database)

---

## Requirements

- Python 3.9+ (stdlib only for the scripts; no extra packages required)  
- Optional: Unsloth Studio / any SFT trainer for fine-tuning  
- Optional: NVIDIA GPU for local QLoRA (Nemotron 3 Nano 4B fits consumer VRAM under QLoRA)

---

## Attribution

© 2026 **Knatware Technology UK**  
Developed by **Kayode Okosi**, LLM Developer  

MIT License — see `LICENSE`.

When using, forking or redistributing this work, please retain the attribution notice in `ATTRIBUTION.md`.
