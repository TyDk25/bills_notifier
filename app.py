from flask import Flask, render_template, request, redirect, url_for, Response
from flask_bootstrap import Bootstrap
from message_sender import check_upcoming_bills
from database import Bills, session
from add_new_bill import add_bill_to_database

# Create a Flask app instance
app = Flask(__name__)

# Initialize Bootstrap extension
Bootstrap(app)


@app.route('/')
def index() -> str:
    """
    Loads flask application and gets bills from database to add to table.

    :return: list of bills
    """
    bills = session.query(Bills).all()
    return render_template(template_name_or_list='index.html', bills=bills)


@app.route(rule='/add_bill', methods=['POST'])
def add_bill() -> Response:
    """
    Adds bill to database using HTML Button.
    :return: Response from website.
    """
    bill_name = request.form.get('Name')
    bill_amount = request.form.get('Amount')
    day = int(request.form.get('Day'))
    add_bill_to_database(bill_name, bill_amount, day)

    return redirect(url_for('index'))


@app.route(rule='/delete_bill', methods=['POST'])
def delete_bill() -> Response:
    """
    Deletes bill from database using HTML Button.
    :return: Response from website.
    """
    bill_id = request.form.get('data-bill_id')
    bill_to_delete = session.query(Bills).filter_by(id=bill_id).first()
    if bill_to_delete:
        session.delete(bill_to_delete)
        session.commit()
    return redirect(url_for('index'))


@app.route(rule='/check_upcoming_bills', methods=['POST'])
def check_bills() -> Response:
    """
    Sends SMS message using check_upcoming_bills function.
    :return: Response from website.
    """
    check_upcoming_bills()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
