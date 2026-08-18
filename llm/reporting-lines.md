# Reporting Lines (Lightweight Inference)

The full organogram CSV does **not** contain an explicit `reports_to` column.  
Until the future database provides it, generators use this department → lead map:

| Department                 | Lead (Display Name)     | Title                     |
|----------------------------|-------------------------|---------------------------|
| Executive Office           | Emma Chief              | AI CEO                    |
| Information Technology     | Kayode AI               | IT Director               |
| Crypto & Trading           | Daniel TradeLead        | AI Trading Lead           |
| Finance & Administration   | Michael FinanceControl  | AI Finance Controller     |
| Human Resources            | Harper HRManager        | AI HR Manager             |
| Product Management         | Isabella ProductManager | AI Product Manager        |
| Research & Development     | Jack ResearchLead       | AI Research Lead          |
| Ethics & Compliance        | Hannah EthicsOfficer    | AI Ethics Officer         |
| Strategic Advisory         | Deji AI                 | Human Adviser             |

The AI CEO reports to “top of organisation”.

When a real `reports_to` field is added in the database, scripts will prefer it over these heuristics. The LLM-facing prompt format stays the same.
