# Future Database Mapping

Staff data will eventually move from `organogram.csv` into a database used by the AI-Workforce platform.

## Suggested table (illustrative)

```sql
CREATE TABLE staff (
  id            UUID PRIMARY KEY,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  display_name  TEXT NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  work_phone    TEXT,
  department_id UUID REFERENCES departments(id),
  job_title     TEXT NOT NULL,
  staff_type    TEXT CHECK (staff_type IN ('AI', 'HUMAN')),
  reports_to    UUID REFERENCES staff(id),
  status        TEXT DEFAULT 'ACTIVE',
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);
```

## Migration principles

1. **CSV remains readable** until the cut-over. Generators accept either a CSV path or a DB connection string.
2. **LLM contracts do not change** – system prompts and JSONL message format stay identical; only the data source behind `generate_role_prompts.py` / `csv_to_jsonl.py` changes.
3. **Reporting lines** will be first-class (`reports_to`) once the hierarchy is modelled; until then the scripts infer a lightweight hierarchy from department + job title patterns (see `llm/reporting-lines.md`).
4. **Idempotent seeding** – the same organogram can be re-imported into the DB without breaking existing chat history or adapter IDs.
