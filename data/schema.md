# Organogram CSV Schema (full export)

File: `data/organogram.csv`  
Source: `knatware_organogram_full_03112025A.csv`

| Column           | Used for LLM? | Description |
|------------------|---------------|-------------|
| First Name       | yes           | Given name |
| Last Name        | yes           | Family / key name |
| Display Name     | **yes**       | Preferred name in UI / chat |
| Nickname         | optional      | Often same as primary email local-part |
| Primary Email    | **yes**       | Main corporate email |
| Secondary Email  | optional      | Alternate email |
| Screen Name      | optional      | Sometimes mirrors job title |
| Work Phone       | **yes**       | Internal extension / ID |
| Job Title        | **yes**       | Role title |
| Department       | **yes**       | Organisational unit |
| Organization     | yes           | Always “Knatware Technology UK” |
| **Custom 1**     | **yes**       | Full role brief / system-prompt seed (detailed task description) |
| Notes            | —             | Usually empty in this export; prefer Custom 1 |

Other address / birth / custom columns are present but not required for LLM persona generation.

## Important

- **Current source of truth**: this CSV.
- **Future**: the same fields will live in a database. Generators will switch from CSV to DB; prompt and message formats stay the same.
- Role briefs in **Custom 1** are the richest source for system prompts and fine-tuning examples.
