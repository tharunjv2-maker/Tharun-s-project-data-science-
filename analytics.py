"""
Business Intelligence & Reporting Module (analytics.py)
Computes data quality diagnostics, telecom prefix distributions,
and email domain analytics using pure Python datastructures.
"""

def generate_analytics_report(total_processed: int, valid_records: list[dict], rejected_log: list[dict]) -> str:
    """
    Generates a structured ASCII Business Intelligence summary report.
    """
    valid_count = len(valid_records)
    rejected_count = len(rejected_log)
    accuracy_rate = (valid_count / total_processed * 100) if total_processed > 0 else 0.0

    # Telecom Breakdown
    telecom_series = {"9-Series": 0, "8-Series": 0, "7-Series": 0, "6-Series": 0}
    for rec in valid_records:
        phone = rec.get("phone", "")
        if phone:
            prefix = phone[0] + "-Series"
            if prefix in telecom_series:
                telecom_series[prefix] += 1

    # Email Domain Breakdown
    domain_counts = {}
    for rec in valid_records:
        email = rec.get("email", "")
        if "@" in email:
            domain = "@" + email.split("@")[1].lower()
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

    sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)

    # Rejection Breakdown
    rejection_categories = {}
    for rej in rejected_log:
        reason = rej.get("reason", "Unknown Error")
        if "name" in reason.lower():
            cat = "Missing Name"
        elif "duplicate" in reason.lower():
            cat = "Duplicate Record"
        elif "prefix" in reason.lower() or "digit" in reason.lower() or "phone" in reason.lower():
            cat = "Invalid Phone"
        elif "email" in reason.lower() or "@" in reason or "." in reason:
            cat = "Bad Email"
        else:
            cat = "Other Error"
        rejection_categories[cat] = rejection_categories.get(cat, 0) + 1

    # Format ASCII Report
    report_lines = []
    report_lines.append("=======================================================")
    report_lines.append("      STUDENT REGISTRATION - BUSINESS INTELLIGENCE     ")
    report_lines.append("=======================================================")
    report_lines.append(f"Total Contacts Processed : {total_processed}")
    report_lines.append(f"Valid Registrations      : {valid_count}")
    report_lines.append(f"Rejected Records         : {rejected_count}")
    report_lines.append(f"Data Quality Accuracy    : {accuracy_rate:.1f}%")
    report_lines.append("")
    report_lines.append("--- Rejection Reason Diagnostics ---")
    for cat, count in rejection_categories.items():
        report_lines.append(f"  {cat:<22} : {count} record(s)")
    report_lines.append("")
    report_lines.append("--- Telecom Network Breakdown ---")
    labels = {
        "9-Series": "(e.g. Jio/Airtel)",
        "8-Series": "(e.g. Vi/Airtel)",
        "7-Series": "(e.g. BSNL/Vi)",
        "6-Series": "(e.g. BSNL/Other)"
    }
    for series, label in telecom_series.items():
        unit = "student" if telecom_series[series] == 1 else "students"
        report_lines.append(f"  {series} {label:<18} : {telecom_series[series]} {unit}")
    report_lines.append("")
    report_lines.append("--- Top Email Domains ---")
    for dom, count in sorted_domains:
        unit = "student" if count == 1 else "students"
        report_lines.append(f"  {dom:<22} : {count} {unit}")
    report_lines.append("=======================================================")

    return "\n".join(report_lines)
