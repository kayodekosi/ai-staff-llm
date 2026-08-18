#!/usr/bin/env python3
"""
Convert full organogram into chat JSONL for staff-persona fine-tuning.
Uses Display Name, Job Title, Department, Primary Email, Work Phone, Custom 1.
Product of Knatware Technology UK — Developed by Kayode Okosi, LLM Developer
"""
from __future__ import annotations
import argparse, csv, json
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with args.csv.open(newline="", encoding="utf-8") as f, args.out.open("w", encoding="utf-8") as out:
        for row in csv.DictReader(f):
            if args.max and written >= args.max:
                break
            display = (row.get("Display Name") or "").strip()
            title = (row.get("Job Title") or "").strip()
            dept = (row.get("Department") or "").strip()
            email = (row.get("Primary Email") or "").strip()
            phone = (row.get("Work Phone") or "").strip()
            role_brief = (row.get("Custom 1") or row.get("Notes") or "").strip()
            if not display or not title:
                continue
            mgr_d, mgr_t = DEPT_LEAD.get(dept, ("Emma Chief", "AI CEO"))
            if "CEO" in title.upper():
                mgr_d, mgr_t = ("—", "top of organisation")
            elif display == mgr_d:
                mgr_d, mgr_t = ("Emma Chief", "AI CEO")
            brief_short = (role_brief[:220] + "…") if len(role_brief) > 220 else role_brief
            if not brief_short:
                brief_short = f"Support {dept} objectives as {title}."
            system = (
                f"You are {display}, {title} in the {dept} department at Knatware Technology UK. "
                f"You report to {mgr_d} ({mgr_t}). Role focus: {brief_short} Stay in character and be professional."
            )
            pairs = [
                ("What is your role and which department do you belong to?",
                 f"I am {display}, {title} in the {dept} department at Knatware Technology UK."),
                ("Who do you report to?",
                 f"For organisational purposes I report to {mgr_d}, {mgr_t}."),
                ("How can a colleague reach you?",
                 f"You can reach me at {email or 'n/a'}" + (f" or on extension {phone}." if phone else ".")),
            ]
            if role_brief:
                pairs.append(("What are your main responsibilities?",
                              role_brief if len(role_brief) < 600 else role_brief[:600] + "…"))
            for user, asst in pairs:
                ex = {"messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": asst},
                ]}
                out.write(json.dumps(ex, ensure_ascii=False) + "\n")
            written += 1
    print(f"Wrote fine-tuning examples for {written} staff members → {args.out}")

if __name__ == "__main__":
    main()
