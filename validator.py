"""
Validator Engine Module (validator.py)
Implements Flowchart 1 logic sequence for contact validation.
"""

def validate_contact(name: str, phone: str, email: str) -> tuple[bool, str]:
    """
    Validates contact fields against strict business rules:
    - Name: Non-blank, non-whitespace.
    - Phone: Exactly 10 digits, numeric only, starts with 6, 7, 8, or 9.
    - Email: Exactly one '@', no whitespace, non-empty username before '@', 
             domain contains a '.' not at the start or end.
    
    Returns: (is_valid: bool, reason: str)
    """
    # 1. Validate Name
    clean_name = name.strip() if name else ""
    if not clean_name:
        return False, "Student name is missing/blank"

    # 2. Validate Phone
    clean_phone = phone.strip() if phone else ""
    if not clean_phone:
        return False, "Phone number is missing/empty"
    
    if len(clean_phone) != 10 or not clean_phone.isdigit():
        return False, f"Invalid phone format '{clean_phone}' (must be exactly 10 digits)"
    
    if clean_phone[0] not in ('6', '7', '8', '9'):
        return False, f"Invalid phone prefix '{clean_phone[0]}' (must start with 6, 7, 8, or 9)"

    # 3. Validate Email
    clean_email = email.strip() if email else ""
    if not clean_email:
        return False, "Email is missing/empty"
    
    if " " in clean_email or "\t" in clean_email or "\n" in clean_email:
        return False, "Email contains invalid whitespace"

    if clean_email.count("@") != 1:
        return False, "Email must contain exactly one '@' character"

    local_part, domain_part = clean_email.split("@")
    
    if not local_part:
        return False, "Email username before '@' is missing"

    if not domain_part:
        return False, "Email domain after '@' is missing"

    if "." not in domain_part:
        return False, "Email domain part must contain a '.' character"

    if domain_part.startswith(".") or domain_part.endswith("."):
        return False, "Email domain cannot start or end with a '.' period"

    return True, "Valid"
