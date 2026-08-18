#!/usr/bin/env python3
"""
Generate role-aware system prompts from the full Knatware organogram CSV.
Uses Display Name, Job Title, Department, Primary Email, Work Phone, and Custom 1 (role brief).
Product of Knatware Technology UK — Developed by Kayode Okosi, LLM Developer
"""
from __future__ import annotations
import argparse, csv
from pathlib import Path

DEPT_LEAD = {
    "Executive Office": ("Emma Chief", "AI CEO"),
    "Information Technology": ("Kayode AI", "IT Director"),
    "Crypto & Trading": ("Daniel TradeLead", "AI Trading Lead"),
    "Finance & Administration": ("Michael FinanceControl", "AI Finance Controller"),
    "Human Resources": ("Harper HRManager", "AI HR Manager"),
    "Product Management": ("Isabella ProductManager", "AI Product Manager"),
    "Research & Development": ("Jack ResearchLead", "AI Research Lead"),
    "Ethics & Compliance": ("Hannah EthicsOfficer", "AI Ethics Officer"),
    "Strategic Advisory": ("Deji AI", "Human Adviser"),
}

TEMPLATE = """You are {display_name}, {job_title} in the {department} department at Knatware Technology UK.

Your corporate email is {email}. Internal extension / ID: {work_phone}.

You report (for organisational purposes) to: {manager_display} ({manager_title}).

Role brief:
{role_brief}

Stay strictly in character:
- Answer as this role would answer.
- Follow the priorities and responsibilities in the role brief.
- Escalate decisions that belong to your manager or to the AI CEO when appropriate.
- Do not invent company policy; if unsure, say you will check with the relevant lead.
- Be concise, professional and helpful.

You are part of an AI-staffed organisation. Some colleagues are AI agents; some are human. Treat both with the same professional courtesy.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            display = (row.get("Display Name") or "").strip()
            title = (row.get("Job Title") or "").strip()
            dept = (row.get("Department") or "").strip()
            email = (row.get("Primary Email") or row.get("Nickname") or "").strip()
            phone = (row.get("Work Phone") or "").strip()
            role_brief = (row.get("Custom 1") or row.get("Notes") or "").strip()
            if not display or not title:
                continue
            mgr_d, mgr_t = DEPT_LEAD.get(dept, ("Emma Chief", "AI CEO"))
            if "CEO" in title.upper():
                mgr_d, mgr_t = ("—", "top of organisation")
            elif display == mgr_d:
                mgr_d, mgr_t = ("Emma Chief", "AI CEO")
            if not role_brief:
                role_brief = f"As the {title} in the {dept} department at Knatware Technology UK, you support the team's objectives and collaborate across the organisation."
            prompt = TEMPLATE.format(
                display_name=display, job_title=title, department=dept,
                email=email or "n/a", work_phone=phone or "n/a",
                manager_display=mgr_d, manager_title=mgr_t, role_brief=role_brief,
            )
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in display)[:60]
            (args.out / f"{safe}.txt").write_text(prompt, encoding="utf-8")
            count += 1
    print(f"Wrote {count} system prompts to {args.out}")

if __name__ == "__main__":
    main()
