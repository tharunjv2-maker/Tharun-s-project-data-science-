"""
Data Ingestion & Duplicate Handling Module (loader.py)
Reads raw CSV data, filters invalid records, prevents duplicates,
and exports clean student data.
"""

import csv
import os
from validator import validate_contact

def load_contacts(csv_filepath: str = "contacts.csv") -> tuple[list[dict], list[dict], int]:
    """
    Ingests contacts CSV, applies validation logic, rejects duplicates,
    and returns (valid_records, rejected_log, total_rows).
    """
    valid_records = []
    rejected_log = []
    seen_phones = set()
    seen_emails = set()
    seen_phone_owners = {}
    
    total_rows = 0

    if not os.path.exists(csv_filepath):
        print(f"Error: Target CSV file '{csv_filepath}' not found.")
        return [], [], 0

    with open(csv_filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        student_id_counter = 1001

        for row in reader:
            total_rows += 1
            name = row.get("name", "").strip()
            phone = row.get("phone", "").strip()
            email = row.get("email", "").strip()

            is_valid, reason = validate_contact(name, phone, email)

            if not is_valid:
                rejected_log.append({
                    "row_num": total_rows,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "reason": reason,
                    "category": "Validation Failure"
                })
                continue

            # Check for duplicates
            if phone in seen_phones:
                owner = seen_phone_owners.get(phone, "another student")
                rejected_log.append({
                    "row_num": total_rows,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "reason": f"Phone number {phone} already registered to {owner}",
                    "category": "Duplicate Phone"
                })
                continue

            if email in seen_emails:
                rejected_log.append({
                    "row_num": total_rows,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "reason": f"Email address {email} already registered",
                    "category": "Duplicate Email"
                })
                continue

            # Accept Record
            seen_phones.add(phone)
            seen_emails.add(email)
            seen_phone_owners[phone] = name

            record = {
                "id": str(student_id_counter),
                "name": name,
                "phone": phone,
                "email": email
            }
            valid_records.append(record)
            student_id_counter += 1

    return valid_records, rejected_log, total_rows

def save_clean_contacts(records: list[dict], output_filepath: str = "students_clean.csv") -> bool:
    """Writes clean student list of dicts to CSV."""
    fieldnames = ["id", "name", "phone", "email"]
    try:
        with open(output_filepath, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        return True
    except Exception as e:
        print(f"Failed to write to '{output_filepath}': {e}")
        return False

def print_ingestion_summary(total_rows: int, valid_records: list[dict], rejected_log: list[dict]):
    """Displays detailed terminal log of the ingestion process."""
    print("=" * 70)
    print("            CSV DATA INGESTION & DIAGNOSTIC REPORT            ")
    print("=" * 70)
    print(f"Total Rows Read     : {total_rows}")
    print(f"Valid Rows Accepted : {len(valid_records)}")
    print(f"Rejected Records    : {len(rejected_log)}")
    print("-" * 70)
    print("REJECTION DIAGNOSTIC LOG:")
    print(f"{'Row':<5} | {'Name':<15} | {'Phone':<12} | {'Diagnostic Reason'}")
    print("-" * 70)
    for rej in rejected_log:
        r_name = rej['name'] if rej['name'] else "<BLANK>"
        r_phone = rej['phone'] if rej['phone'] else "<EMPTY>"
        print(f"{rej['row_num']:<5} | {r_name:<15} | {r_phone:<12} | {rej['reason']}")
    print("=" * 70)
