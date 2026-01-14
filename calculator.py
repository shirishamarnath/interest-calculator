from datetime import datetime
import calendar
import math

ANNUAL_RATE = 0.12
DAYS_IN_YEAR = 360.0
DAYS_IN_MONTH = 30.0
MONTHLY_RATE = ANNUAL_RATE * (DAYS_IN_MONTH / DAYS_IN_YEAR)

def parse_date_loose(s: str) -> datetime:
    """
    Accept yyyy-mm-dd (from HTML date input),
    dd/mm/yyyy or dd/mm/yy
    """
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError("Invalid date format")

def last_day_of_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]

def add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, last_day_of_month(year, month))
    return datetime(year, month, day)

def calc_calendar_months_and_days(given: datetime, release: datetime):
    if release < given:
        raise ValueError("Release date must be on or after the given date.")
    months = (release.year - given.year) * 12 + (release.month - given.month)
    if release.day < given.day:
        months -= 1
    anchor = add_months(given, months)
    days = (release - anchor).days
    return months, days

def round_half_up(x: float) -> int:
    return math.floor(x + 0.5)

def compute_interest_with_paid_months(amount: float, months: int, days: int, months_paid: int) -> dict:
    if months == 0 and days > 0:
        days_for_interest = 30
    else:
        days_for_interest = months * 30 + days

    gross_interest = (amount * ANNUAL_RATE * days_for_interest) / DAYS_IN_YEAR
    one_month_interest = amount * MONTHLY_RATE
    amount_already_paid = months_paid * one_month_interest

    net_interest = gross_interest - amount_already_paid
    if net_interest < 0:
        net_interest = 0.0

    total_payable_raw = amount + net_interest
    total_payable = round_half_up(total_payable_raw)

    return {
        "net_interest": round(net_interest, 2),
        "total_payable": total_payable
    }

# 🔥 THIS IS THE FUNCTION FASTAPI WILL CALL
def calculate_interest(
    given_date: str,
    release_date: str,
    amount: float,
    additional_interest_paid: int
) -> dict:

    given = parse_date_loose(given_date)
    release = parse_date_loose(release_date)

    months, days = calc_calendar_months_and_days(given, release)

    # default 1 month + additional paid
    months_paid = 1 + additional_interest_paid

    leftover_months = months - additional_interest_paid - 1
    if leftover_months < 0:
        leftover_months = 0

    interest_data = compute_interest_with_paid_months(
        amount=amount,
        months=months,
        days=days,
        months_paid=months_paid
    )

    return {
        "calendar_months": months,
        "leftover_months": leftover_months,
        "leftover_days": days,
        "net_interest": interest_data["net_interest"],
        "total_payable": interest_data["total_payable"]
    }
