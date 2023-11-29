from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from Website.menu_items import sql_menu_update 
import re
import mysql.connector


menu_db = mysql.connector.connect(
host="localhost",
user="root",
passwd="root",
database="POS"
)
cur = menu_db.cursor(buffered=True)


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    enteredPin = request.form.get('pin')
    if request.method == 'POST':
        try:
            # Check manager PIN
            cur.execute(f"SELECT pin FROM manager WHERE '{enteredPin}' IN (pin)")
            menu_db.commit()
            if len(enteredPin) == 0: 
                flash("PIN cannot be blank.")

            for x in cur:
                if enteredPin not in x:
                    flash('Invalid pin, try again.', category='error')
                else:
                    flash('Login successful!', category='success')
                    return render_template("Manager.html")

        except Exception as e:
            flash(f'Error checking manager PIN: {e}', category='error')

        try:
            # Check employee PIN
            cur.execute(f"SELECT pin FROM Employees WHERE '{enteredPin}' IN (pin)")
            menu_db.commit()
            if len(enteredPin) == 0: 
                flash("PIN cannot be blank.")

            for x in cur:
                if enteredPin not in x:
                    flash('Invalid pin, try again.', category='error')
                else:
                    return render_template("menu_add.html")

        except Exception as e:
            flash(f'Error checking employee PIN: {e}', category='error')
        cur.close
        menu_db.close

    return render_template("login.html", boolean=True)


# @auth.route('/manager', methods=['GET', 'POST'])
# def manager():
#     return render_template("Manager.html")

@auth.route('/Addemp', methods=['GET', 'POST'])
def addemp():
    if request.method == 'POST':
        try:
            fname = request.form.get('firstname')
            lname = request.form.get('lastname')
            pin1 = request.form.get('Pin1')
            pin2 = request.form.get('Pin2')

            if len(fname) == 0:
                flash('Insert valid first name', category='error')
            elif len(lname) == 0:
                flash('Insert valid last name', category='error')
            elif len(pin1) == 0:
                flash('Insert valid pin', category='error')
            elif pin1 != pin2:
                flash('Pins do not match', category='error')
            else:
                # Insert employee data into the 'employees' table
                cur.execute("INSERT INTO employees (firstname, lastname, pin) VALUES (%s, %s, %s)",
                            (fname, lname, pin1))

                menu_db.commit()
                flash('Employee Added!', category='success')

        except Exception as e:
            flash(f'Error adding employee: {e}', category='error')

        cur.close
        menu_db.close
    return render_template("AddEmp.html")

def remove_employee(employee_id_to_remove):
    try:
        # Assuming 'employees' is your table name and 'id' is the primary key
        cur.execute("DELETE FROM employees WHERE employeeID = %s", (employee_id_to_remove,))
        menu_db.commit()

        flash('Employee Removed!', category='success')
    except Exception as e:
        flash(f'Error removing employee: {e}', category='error')

@auth.route('/remove_employee', methods=['GET', 'POST'])
def remove_employee_route():
    if request.method == 'POST':
        try:
            employee_id_to_remove = int(request.form.get('remove_employee_id'))
            remove_employee(employee_id_to_remove)

        except Exception as e:
            flash(f'Error during employee removal: {e}', category='error')

    # Fetch the updated employee list after removal
    try:
        cur.execute("SELECT * FROM employees")
        employee_list = cur.fetchall()
        return render_template('RemEmp.html', employee_list=employee_list)

    except Exception as e:
        flash(f'Error fetching employee list: {e}', category='error')

    finally:
        cur.close()  # Close the cursor
        menu_db.close()