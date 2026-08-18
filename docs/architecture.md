# Architecture

## Current state

```
organogram.csv  ──►  generate_role_prompts.py  ──►  per-staff system prompts
                 └──►  csv_to_jsonl.py          ──►  chat JSONL for SFT / QLoRA
```

- **Source of truth**: `data/organogram.csv`
- **LLM layer**: role-aware system prompts + optional small adapters (PASTA / Unsloth / Nemotron)
- **Runtime**: AI-Workforce platform loads staff and can inject the generated prompts (or call a fine-tuned adapter)

## Future state (database)

```
staff table (DB)  ──►  same generators (CSV path or DB connection)  ──►  same prompts & JSONL
```

The LLM-facing contracts do not change. Only the reader behind the generators switches from CSV to SQL/ORM.

## Reporting lines

Until `reports_to` exists in the database, a lightweight department→lead map is used (see `llm/reporting-lines.md`). This is enough for coherent persona behaviour and escalation language.
