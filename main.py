"""
Interactive Student Management Console (main.py)
Menu-driven CLI application for coaching institute coordinators.
"""

import sys
import os
from validator import validate_contact
from loader import load_contacts, save_clean_contacts, print_ingestion_summary
from analytics import generate_analytics_report

def print_menu():
    print("\n" + "=" * 50)
    print(" STUDENT REGISTRATION & CONTACT INTELLIGENCE SYSTEM ")
    print("=" * 50)
    print(" 1. View All Students")
    print(" 2. Search Student Record")
    print(" 3. Register New Student")
    print(" 4. Update Existing Student")
    print(" 5. Delete Student Record")
    print(" 6. Run Business Intelligence Analytics")
    print(" 7. Save & Exit")
    print("=" * 50)

def view_all_students(students: list[dict]):
    print("\n--- REGISTERED STUDENTS DATABASE ---")
    if not students:
        print("No student records available.")
        return
    print(f"{'ID':<6} | {'Name':<20} | {'Phone':<12} | {'Email':<30}")
    print("-" * 75)
    for s in students:
        print(f"{s['id']:<6} | {s['name']:<20} | {s['phone']:<12} | {s['email']:<30}")
    print(f"Total Active Students: {len(students)}")

def search_student(students: list[dict]):
    print("\n--- SEARCH STUDENT RECORD ---")
    query = input("Enter Name, Phone Number, or Email to search: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return
    results = [
        s for s in students
        if query in s["name"].lower() or query in s["phone"].lower() or query in s["email"].lower()
    ]
    if not results:
        print(f"No records matching '{query}' found.")
    else:
        print(f"Found {len(results)} matching record(s):")
        print(f"{'ID':<6} | {'Name':<20} | {'Phone':<12} | {'Email':<30}")
        print("-" * 75)
        for s in results:
            print(f"{s['id']:<6} | {s['name']:<20} | {s['phone']:<12} | {s['email']:<30}")

def register_student(students: list[dict], seen_phones: set, seen_emails: set):
    print("\n--- REGISTER NEW STUDENT ---")
    name = input("Enter Student Name: ").strip()
    phone = input("Enter 10-Digit Phone: ").strip()
    email = input("Enter Email Address: ").strip()

    is_valid, reason = validate_contact(name, phone, email)
    if not is_valid:
        print(f"❌ Registration Failed: {reason}")
        return

    if phone in seen_phones:
        print(f"❌ Registration Failed: Phone number '{phone}' is already registered.")
        return
    if email in seen_emails:
        print(f"❌ Registration Failed: Email address '{email}' is already registered.")
        return

    # Generate new ID
    max_id = max([int(s["id"]) for s in students], default=1000)
    new_id = str(max_id + 1)

    new_student = {"id": new_id, "name": name, "phone": phone, "email": email}
    students.append(new_student)
    seen_phones.add(phone)
    seen_emails.add(email)

    print(f"✅ Success: Student '{name}' registered successfully with ID {new_id}!")

def update_student(students: list[dict], seen_phones: set, seen_emails: set):
    print("\n--- UPDATE STUDENT RECORD ---")
    target_id = input("Enter Student ID or Phone Number to update: ").strip()
    target_student = None
    for s in students:
        if s["id"] == target_id or s["phone"] == target_id:
            target_student = s
            break
    
    if not target_student:
        print(f"❌ Error: Student matching '{target_id}' not found.")
        return

    print(f"Current Record: ID {target_student['id']} | Name: {target_student['name']} | Phone: {target_student['phone']} | Email: {target_student['email']}")
    new_name = input(f"Enter New Name (leave blank to keep '{target_student['name']}'): ").strip()
    new_phone = input(f"Enter New Phone (leave blank to keep '{target_student['phone']}'): ").strip()
    new_email = input(f"Enter New Email (leave blank to keep '{target_student['email']}'): ").strip()

    updated_name = new_name if new_name else target_student['name']
    updated_phone = new_phone if new_phone else target_student['phone']
    updated_email = new_email if new_email else target_student['email']

    is_valid, reason = validate_contact(updated_name, updated_phone, updated_email)
    if not is_valid:
        print(f"❌ Update Failed: {reason}")
        return

    # Duplicate check if phone changed
    if updated_phone != target_student['phone'] and updated_phone in seen_phones:
        print(f"❌ Update Failed: Phone number '{updated_phone}' is already registered to another student.")
        return

    # Duplicate check if email changed
    if updated_email != target_student['email'] and updated_email in seen_emails:
        print(f"❌ Update Failed: Email address '{updated_email}' is already registered to another student.")
        return

    # Update state
    seen_phones.remove(target_student['phone'])
    seen_emails.remove(target_student['email'])
    
    target_student['name'] = updated_name
    target_student['phone'] = updated_phone
    target_student['email'] = updated_email
    
    seen_phones.add(updated_phone)
    seen_emails.add(updated_email)

    print(f"✅ Success: Student ID {target_student['id']} updated successfully!")

def delete_student(students: list[dict], seen_phones: set, seen_emails: set):
    print("\n--- DELETE STUDENT RECORD ---")
    target = input("Enter Student ID or Phone Number to delete: ").strip()
    target_student = None
    for s in students:
        if s["id"] == target or s["phone"] == target:
            target_student = s
            break
    
    if not target_student:
        print(f"❌ Error: Student matching '{target}' not found.")
        return

    confirm = input(f"Are you sure you want to delete {target_student['name']} (ID: {target_student['id']})? (y/n): ").strip().lower()
    if confirm == 'y':
        students.remove(target_student)
        seen_phones.remove(target_student['phone'])
        seen_emails.remove(target_student['email'])
        print(f"✅ Success: Student record ID {target_student['id']} safely deleted.")
    else:
        print("Deletion cancelled.")

def main():
    csv_file = "contacts.csv"
    clean_csv_file = "students_clean.csv"
    
    print("Initializing Student Registration & Contact Intelligence System...")
    students, rejected_log, total_processed = load_contacts(csv_file)
    print_ingestion_summary(total_processed, students, rejected_log)
    save_clean_contacts(students, clean_csv_file)

    seen_phones = {s["phone"] for s in students}
    seen_emails = {s["email"] for s in students}

    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            view_all_students(students)
        elif choice == '2':
            search_student(students)
        elif choice == '3':
            register_student(students, seen_phones, seen_emails)
            save_clean_contacts(students, clean_csv_file)
        elif choice == '4':
            update_student(students, seen_phones, seen_emails)
            save_clean_contacts(students, clean_csv_file)
        elif choice == '5':
            delete_student(students, seen_phones, seen_emails)
            save_clean_contacts(students, clean_csv_file)
        elif choice == '6':
            report = generate_analytics_report(total_processed, students, rejected_log)
            print("\n" + report)
        elif choice == '7':
            save_clean_contacts(students, clean_csv_file)
            print(f"\nData saved to '{clean_csv_file}'. Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please select a number between 1 and 7.")

if __name__ == "__main__":
    main()
