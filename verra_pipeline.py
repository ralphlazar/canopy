#!/usr/bin/env python3
"""
Verra Pipeline - Canopy
Reads a CSV exported from the Verra registry search page.
Compares against projects.json and drafts pending entries for any new African projects.

Usage:
    python3 verra_pipeline.py \
        --csv ~/Downloads/verra_export.csv \
        --projects /Users/lisaswerling/RALPH/AI/canopy/data/projects.json \
        --output ~/Downloads/projects_pending.json \
        [--afolu-only] [--active-only]
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import date

AFOLU_TYPE = "agriculture forestry and other land use"

ACTIVE_STATUSES = {
    "registered",
    "under validation",
    "under development",
    "registration requested",
    "verification approval requested",
    "registration and verification approval requested",
    "crediting period renewal",
}


def slugify(name):
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def clean_credits(raw):
    if not raw:
        return "Unknown"
    raw = raw.strip().strip('"').replace(",", "")
    try:
        n = float(raw)
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M tCO2e/yr"
        if n >= 1_000:
            return f"{int(n):,} tCO2e/yr"
        return f"{int(n):,} tCO2e/yr"
    except ValueError:
        return raw


def normalise_status(raw):
    raw = raw.strip().lower()
    mapping = {
        "registered": "Registered",
        "under validation": "Under validation",
        "under development": "Under development",
        "registration requested": "Registration Requested",
        "verification approval requested": "Verification Approval Requested",
        "registration and verification approval requested": "Registration And Verification Approval Requested",
        "crediting period renewal": "Crediting period renewal",
        "inactive": "Inactive",
        "withdrawn": "Withdrawn",
        "rejected": "Rejected",
        "late to verify": "Late To Verify",
        "on hold": "On Hold",
        "units transferred": "Units Transferred",
    }
    for key, label in mapping.items():
        if key in raw:
            return label
    return raw.title()


def is_active(raw_status):
    s = raw_status.strip().lower()
    for active in ACTIVE_STATUSES:
        if active in s:
            return True
    return False


def normalise_methodology(raw):
    raw = raw.strip()
    if not raw:
        return "Unknown"
    parts = [p.strip() for p in re.split(r"[,;]", raw) if p.strip()]
    return " / ".join(parts)


def draft_entry(row, verra_id):
    name = row.get("Name", "").strip()
    country = row.get("Country/Area", "").strip()
    methodology = normalise_methodology(row.get("Methodology", ""))
    status = normalise_status(row.get("Status", ""))
    credits = clean_credits(row.get("Estimated Annual Emission Reductions", ""))
    afolu = row.get("AFOLU Activities", "").strip()

    tags = []
    if methodology and methodology != "Unknown":
        tags.append(methodology)
    if afolu:
        tags.append(afolu)
    if status:
        tags.append(status)

    return {
        "id": slugify(name),
        "name": name.title() if name.isupper() else name,
        "country": country,
        "region": "",
        "methodology": methodology,
        "credits": credits,
        "area": "",
        "certification": "VCS",
        "status": status,
        "tags": tags,
        "featured": False,
        "verra_id": verra_id,
        "_draft": True,
        "_drafted": date.today().isoformat(),
    }


def load_existing(projects_path):
    if not os.path.exists(projects_path):
        print(f"Warning: {projects_path} not found. All projects will be treated as new.")
        return set(), set()
    with open(projects_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    ids = {p["id"] for p in data.get("projects", [])}
    verra_ids = {str(p["verra_id"]) for p in data.get("projects", []) if "verra_id" in p}
    return ids, verra_ids


def main():
    parser = argparse.ArgumentParser(description="Verra pipeline - Canopy (CSV mode)")
    parser.add_argument("--csv", required=True, help="Path to Verra registry CSV export")
    parser.add_argument("--projects", required=True, help="Path to projects.json")
    parser.add_argument("--output", required=True, help="Path to write projects_pending.json")
    parser.add_argument("--afolu-only", action="store_true", help="Filter to AFOLU projects only (recommended)")
    parser.add_argument("--active-only", action="store_true", help="Exclude withdrawn, inactive, late-to-verify, rejected projects")
    args = parser.parse_args()

    print("Canopy - Verra pipeline (CSV mode)")
    print(f"Date: {date.today().isoformat()}")
    filters = []
    if args.afolu_only:
        filters.append("AFOLU only")
    if args.active_only:
        filters.append("active statuses only")
    if filters:
        print(f"Filters: {', '.join(filters)}")
    print()

    existing_ids, existing_verra_ids = load_existing(args.projects)
    print(f"Existing projects in database: {len(existing_ids)}")

    csv_path = os.path.expanduser(args.csv)
    if not os.path.exists(csv_path):
        print(f"Error: CSV not found at {csv_path}")
        sys.exit(1)

    candidates = []
    total_rows = 0
    excluded_type = 0
    excluded_status = 0

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if row.get("Region", "").strip().lower() != "africa":
                continue
            if args.afolu_only:
                if row.get("Project Type", "").strip().lower() != AFOLU_TYPE:
                    excluded_type += 1
                    continue
            if args.active_only:
                if not is_active(row.get("Status", "")):
                    excluded_status += 1
                    continue
            candidates.append(row)

    print(f"Rows in CSV: {total_rows}")
    if args.afolu_only:
        print(f"Non-AFOLU excluded: {excluded_type}")
    if args.active_only:
        print(f"Inactive/withdrawn/rejected excluded: {excluded_status}")
    print(f"Projects to check: {len(candidates)}")
    print()

    new_entries = []
    skipped = []

    for row in candidates:
        verra_id = str(row.get("ID", "")).strip()
        entry = draft_entry(row, verra_id)
        if entry["id"] in existing_ids or verra_id in existing_verra_ids:
            skipped.append(entry["name"])
            continue
        new_entries.append(entry)

    print(f"Already in database (skipped): {len(skipped)}")
    print(f"New projects to review: {len(new_entries)}")
    print()

    # --- NEW: Find existing projects not matched in Verra CSV ---
    verra_names_in_csv = {row.get("Name", "").strip().lower() for row in candidates}
    verra_ids_in_csv = {str(row.get("ID", "")).strip() for row in candidates}

    with open(args.projects, "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    unverified = []
    for p in existing_data.get("projects", []):
        pid = str(p.get("verra_id", "")).strip()
        pname = p.get("name", "").strip().lower()
        matched_by_id = pid and pid in verra_ids_in_csv
        matched_by_name = any(
            pname in vname or vname in pname
            for vname in verra_names_in_csv
            if len(vname) > 4
        )
        if not matched_by_id and not matched_by_name:
            unverified.append({"id": p["id"], "name": p["name"], "country": p.get("country",""), "status": p.get("status","")})

    if unverified:
        print(f"--- UNVERIFIED: {len(unverified)} existing projects with no match in Verra CSV ---")
        print("These may be synthetic, non-Verra, or named differently on the registry.")
        print()
        for u in unverified:
            print(f"  ? {u['name']} ({u['country']}) [{u['status']}]  id:{u['id']}")
        print()

        unverified_output = {
            "_note": "These existing projects were not matched in the Verra CSV. Review each: may be synthetic, registered under a different name, or on a non-Verra standard (Gold Standard, Plan Vivo).",
            "_generated": date.today().isoformat(),
            "unverified_count": len(unverified),
            "projects": unverified
        }
        unverified_path = os.path.expanduser(args.output.replace(".json", "_unverified.json"))
        with open(unverified_path, "w", encoding="utf-8") as f:
            json.dump(unverified_output, f, indent=2, ensure_ascii=False)
        print(f"Unverified list written to: {unverified_path}")
        print()

    if new_entries:
        print("New projects found:")
        for e in new_entries:
            print(f"  - {e['name']} ({e['country']}) [{e['status']}]  verra_id:{e['verra_id']}")
        print()

        output = {
            "_note": "Review before adding to projects.json. Remove _draft and _drafted fields when approving. Fill in region and area where known.",
            "_generated": date.today().isoformat(),
            "_source_csv": os.path.basename(args.csv),
            "pending_count": len(new_entries),
            "projects": new_entries,
        }

        output_path = os.path.expanduser(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"Written to: {output_path}")
    else:
        print("No new projects found. Database is current.")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
