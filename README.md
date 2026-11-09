# Student Registration & Contact Intelligence System
**Course:** Semester 1 BCA • Python Programming Lab Assessment  
**Institution:** Christ Academy Institute for Advanced Studies (CAIAS)  
**Facilitator:** Prof. Jijo Varghese Malayil  
**Maximum Marks:** 30 Marks (Project Execution: 15 Marks | Viva Voce: 15 Marks)

---

## 📌 Project Architecture & Overview
The **Student Registration & Contact Intelligence System** is a modular Python-based data ingestion, validation, management, and Business Intelligence reporting engine. It processes offline registration spreadsheet leads (`contacts.csv`), filters out malformed data records, rejects duplicate phone numbers/emails, allows real-time student management via a menu-driven CLI, and generates executive business intelligence summary metrics for coaching institute coordinators.

### 🌳 Directory Structure
```
student_registration/
├── contacts.csv           # Raw 20-row incoming contact spreadsheet
├── students_clean.csv     # Output database file containing validated, non-duplicate student records
├── validator.py           # Modular validation engine (implements Flowchart 1 logic)
├── loader.py              # Ingestion script: reads CSV, validates, filters duplicates, logs diagnostic reasons
├── analytics.py           # Business Intelligence & summary statistics engine (implements Flowchart 2)
├── main.py                # Interactive menu-driven console application
├── proof/                 # System execution logs & testing evidence
│   ├── console_output.txt # Saved execution console logs
│   └── test_cases.txt     # Validation logic unit test suite results
└── README.md              # Project documentation, setup guide, architecture & viva notes
```

---

## ⚙️ Core Logic Specifications & Validation Rules

### 1. Decision Logic Pipeline (`validator.py`)
Each incoming registration row is validated against strict criteria:
* **Name:** Must not be blank or contain only whitespace (`len(name.strip()) > 0`).
* **Phone:** Must be exactly 10 digits long, numeric only (`phone.isdigit()`), and start with `6`, `7`, `8`, or `9`.
* **Email:** Must contain exactly one `@` symbol, contain no whitespace, have characters before the `@`, and the domain part after `@` must contain a period (`.`) that is not the first or last character.

### 2. Ingestion & Duplicate Handling (`loader.py`)
* Uses Python's built-in `csv.DictReader` to parse input files.
* Maintains hash sets (`seen_phones`, `seen_emails`) for fast **$O(1)$ duplicate lookups**.
* Rejects duplicate phone numbers and email addresses, attributing original owner info.
* Writes valid clean entries with auto-incremented student IDs to `students_clean.csv`.

### 3. Business Intelligence Engine (`analytics.py`)
Aggregates key metrics using core Python data structures:
* **Data Quality Diagnostic:** Computes Total Processed, Acceptance Rate (%), and categorized rejection reasons.
* **Telecom Network Distribution:** Analyzes prefix series (9-Series, 8-Series, 7-Series, 6-Series).
* **Email Domain Breakdown:** Aggregates and ranks top domain extensions (`@gmail.com`, `@outlook.com`, `@yahoo.com`, etc.).

---

## 🚀 How to Run the Application

### Prerequisites
* Python 3.8+ (No external third-party libraries required; uses pure Python standard libraries: `csv`, `sys`, `os`).

### Execution Steps
1. Open terminal inside the `student_registration/` directory.
2. Run the interactive console application:
   ```bash
   python3 main.py
   ```
3. Use the menu options (1–7) to manage student records and view analytics.

---

## 📊 Sample Execution Output Preview

```
=======================================================
      STUDENT REGISTRATION - BUSINESS INTELLIGENCE     
=======================================================
Total Contacts Processed : 20
Valid Registrations      : 13
Rejected Records         : 7
Data Quality Accuracy    : 65.0%

--- Rejection Reason Diagnostics ---
  Missing Name           : 1 record(s)
  Invalid Phone          : 2 record(s)
  Bad Email              : 3 record(s)
  Duplicate Record       : 1 record(s)

--- Telecom Network Breakdown ---
  9-Series (e.g. Jio/Airtel)  : 7 students
  8-Series (e.g. Vi/Airtel)   : 3 students
  7-Series (e.g. BSNL/Vi)     : 2 students
  6-Series (e.g. BSNL/Other)  : 1 student

--- Top Email Domains ---
  @gmail.com             : 7 students
  @outlook.com           : 3 students
  @yahoo.com             : 2 students
  @domain.com            : 1 student
=======================================================
```

---

## 🎓 Key Viva Voce Concepts & Answers

1. **Why store phone numbers as `str` instead of `int`?**
   * Storing phone numbers as strings preserves leading zeroes, allows direct `.isdigit()` and `len()` string validations, and prevents accidental arithmetic operations.

2. **Why use `csv.DictReader` over `csv.reader`?**
   * `DictReader` maps CSV rows to Python dictionaries using header column names as keys, making the code clean, robust, and readable compared to rigid numeric index lookups.

3. **How do Python sets achieve $O(1)$ duplicate checking?**
   * Sets use internal hash tables. Key lookups in sets take $O(1)$ constant time on average, regardless of whether the dataset has 10 or 10,000 records.

4. **Why modularize validation into `validator.py`?**
   * Modularization separates validation rules from file input/output logic, allowing independent testing, reuse across CLI/GUI/API interfaces, and easier maintenance.

---

## 📋 Evaluation Checklist Verification
- [x] **Modular Python Code:** Clean modules (`validator.py`, `loader.py`, `analytics.py`, `main.py`).
- [x] **Input CSV:** `contacts.csv` included and properly ingested.
- [x] **BI Analytics:** Accuracy rate, telecom distribution, and domain ranks calculated cleanly.
- [x] **Testing Evidence:** `proof/console_output.txt` and `proof/test_cases.txt` generated.
- [x] **Documentation:** Detailed README.md provided for review.
