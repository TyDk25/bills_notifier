from datetime import datetime, date, timedelta
from typing import Union, Any
import pandas as pd
from database import engine
from database import Bills, session
from text_message import send_message


class BillsManager:
    """
    Class that handles creating, adding and checking bills in a database.
    """

    def __init__(self):
        self.session = session
        self.engine = engine

    @staticmethod
    def create_bills() -> list[dict[str, Union[Union[date, datetime], Any]]]:
        """
        Creates a list of dictionaries representing bills with their names, amounts, and due dates.

        :return: total_bills
        """
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        all_bills = {
            'Names': ['Raylo', 'Car Insurance', 'Phone', 'Spotify', 'Road Tax', 'YouTube', 'Virgin', 'Golds Gym',
                      'Vodafone'],
            'Days': [23, 25, 25, 26, 1, 3, 8, 8, 11],
            'Amounts': [20, 212, 35, 18, 35, 7, 30, 30, 10]
        }

        total_bills = []

        for name, amount, days in zip(all_bills['Names'], all_bills['Amounts'], all_bills['Days']):
            bill_date = datetime(current_year, current_month, days)

            if bill_date < datetime.today():
                if current_month == 12:
                    current_year += 1
                    bill_date = datetime(current_year, 1, days).date()
                else:
                    bill_date = datetime(current_year, current_month + 1,
                                         days).date()

            bill = {
                'Bill_Name': name,
                'Bill_Amount': amount,
                'Bill_Date': bill_date
            }

            total_bills.append(bill)

        return total_bills

    @staticmethod
    def update_bills_database(name: str, amount: int, day: int, commit: bool = True) -> None:
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

    def add_bills_to_database(self, prompt=True, commit=True) -> None:
        """
        Adds predefined bills to database, prompts user to add any new bills if they wish.

        :param prompt: Asks user whether they want to add a new bill to the database.
        :param commit: Commits session ot database.
        :return: None
        """
        with session.begin():
            session.query(Bills).delete()
            while True:
                if prompt:
                    add_bill = input('Would you like to add another bill? (Y/N): ').strip()
                    try:
                        if add_bill.upper() == 'Y':
                            name = input('Enter bill name: ')
                            amount = int(input('Enter amount: '))
                            day = int(input('Enter day due: '))
                            if self.update_bills_database(name, amount, day, commit=False):
                                self.create_bills()

                        elif add_bill.upper() == 'N':
                            break
                        else:
                            print("Invalid input, please enter 'Y' or 'N'.")
                    except ValueError:
                        print('Please enter a number for amount and date.')
                        break

            for bill in self.create_bills():
                bill_record = Bills(**bill)
                session.add(bill_record)

            # Commit the session to save the changes
        if commit:
            session.commit()

    def get_database_contents(self) -> None:
        """
        Gets contents of Bills table and prints it using Pandas DataFrame.

        :return: None
        """
        with self.engine.connect() as conn:
            print(pd.read_sql_table(table_name='Bills', con=conn))

    @staticmethod
    def check_upcoming_bills() -> None:
        """
        Queries the database and sends SMS message using twilio API if bill payment is due the following day.
        :return: None
        """
        day_in_advance = datetime.today().date() + timedelta(days=1)
        reminders = session.query(Bills).filter(
            Bills.Bill_Date == day_in_advance
        ).all()
        if reminders:
            for bill in reminders:
                reminder_date = f"\nBills Due Tomorrow: \nBill Name: {bill.Bill_Name}\nBill Amount: £{bill.Bill_Amount}"
                send_message(reminder_date)
        else:
            print('No Bills Found')


if __name__ == '__main__':
    bills = BillsManager()
    bills.create_bills()
    bills.add_bills_to_database()
    bills.check_upcoming_bills()
