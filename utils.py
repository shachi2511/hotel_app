from datetime import datetime, date

def validate_email(email):
    return "@" in email and "." in email.split("@")[-1]

def validate_ssn(ssn):
    return ssn.isdigit() and len(ssn) == 9

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def date_range_valid(start_str, end_str):
    if not validate_date(start_str) or not validate_date(end_str):
        return False
    return parse_date(start_str) < parse_date(end_str)

def calculate_total_cost(start_str, end_str, price_per_day):
    start = parse_date(start_str)
    end   = parse_date(end_str)
    days  = (end - start).days
    return round(days * float(price_per_day), 2)

def show_error(message):
    print(f"[ERROR] {message}")

def show_success(message):
    print(f"[OK] {message}")
