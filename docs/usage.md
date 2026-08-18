# Usage

## 1. Generate system prompts for every staff member

```bash
python scripts/generate_role_prompts.py \
  --csv data/organogram.csv \
  --out llm/prompts/generated/
```

Each file is a ready-to-use system prompt encoding name, title, department and inferred manager.

## 2. Build a fine-tuning dataset

```bash
python scripts/csv_to_jsonl.py \
  --csv data/organogram.csv \
  --out llm/datasets/staff_role_sft.jsonl \
  --max 50
```

Load the JSONL into Unsloth Studio (or any SFT trainer). Use the hyperparameters in `llm/pasta-fine-tune/hyperparameters.yaml`.

## 3. Optional: department-level adapters

You can filter the CSV by department before running `csv_to_jsonl.py` to create specialised adapters (e.g. IT-only, Ethics-only). The PASTA loss-curve guidance still applies.

## 4. When the database arrives

Point the same scripts at a DB export or add a `--db` option; keep the prompt and message format identical so existing adapters and chat clients continue to work.
