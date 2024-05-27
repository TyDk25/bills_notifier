from text_message import send_message
from database import session, Bills
from datetime import datetime, timedelta


def check_upcoming_bills() -> None:
    """
    Queries the database and sends SMS message using twilio API if bill payment is due the following day.
    :return: None
    """
    date = datetime.today().date() + timedelta(days=1)
    reminders = session.query(Bills).filter(
        Bills.Bill_Date == date
    ).all()
    if reminders:
        for bill in reminders:
            reminder_date = f"\nBills Due Tomorrow: \nBill Name: {bill.Bill_Name}\nBill Amount: £{bill.Bill_Amount}"
            send_message(reminder_date)
    else:
        print('No Bills Found')



