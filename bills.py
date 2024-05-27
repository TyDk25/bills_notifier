from datetime import datetime
import pandas as pd
from database import engine
from database import Bills, session
from add_new_bill import add_bill_to_database


def create_bills(prompt: bool = True, commit: bool = True) -> None:
    """
    Function that commits dict of bills to sqlalchemy database.

    :param prompt: prompts user for bill, used to stop prompt appearing when Flask app is run.
    :param commit: commits changes to database, used to handle conflicts in Flask application.
    :return: None
    """
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    all_bills = {
        'Names': ['Raylo', 'Car Insurance', 'Phone', 'Spotify', 'Road Tax', 'YouTube', 'Virgin', 'Golds Gym',
                  'Vodafone'],
        'Days': [23, 25, 26, 26, 1, 3, 8, 8, 11],
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
    # Initializes session

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
                        new_bill = add_bill_to_database(name, amount, day, commit=False)
                        if new_bill:
                            total_bills.append(new_bill)

                    elif add_bill.upper() == 'N':
                        break
                    else:
                        print("Invalid input, please enter 'Y' or 'N'.")
                except ValueError:
                    print('Please enter a number for amount and date.')
                    break

        for bill in total_bills:
            bill_record = Bills(**bill)
            session.add(bill_record)

        # Commit the session to save the changes
    if commit:
        session.commit()


def get_table_contents():
    """
    Gets contents of Bills table.

    :return: None
    """
    print(pd.read_sql_table(table_name='Bills', con=engine))


if __name__ == '__main__':
    create_bills()
    get_table_contents()
