from database import *
from datetime import datetime


def add_bill_to_database(name: str, amount: int, day: int, commit: bool = True) -> None:
    """
    :param name: name of bill.
    :param amount: amount of bill.
    :param day: Day bill is due.
    :param commit: Whether we want the changes to be committed.
    :return: None
    """
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    bill_date = datetime(current_year, current_month, day)

    if bill_date < datetime.today():
        bill_date = datetime(current_year, current_month + 1, day).date()
    elif current_month == 12:
        bill_date = datetime(current_year + 1, current_month + 1, day)

    new_bill = {
        'Bill_Name': name,
        'Bill_Amount': amount,
        'Bill_Date': bill_date
    }

    bill_record = Bills(**new_bill)
    session.add(bill_record)

    if commit:
        session.commit()
