from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from Website.menu_items import sql_menu_update 
import re
import mysql.connector

#Connecting Database
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
    entered_pin = request.form.get('pin')

    if request.method == 'POST':
        try:
            # Check manager PIN
            cur.execute("SELECT pin, is_manager FROM Employees WHERE pin = %s", (entered_pin,))
            result = cur.fetchone()

            if result:
                pin, is_manager = result
                if is_manager:
                    flash('Login successful as Manager!', category='success')
                    return render_template("Manager.html")
                else:
                    flash('Invalid pin for Manager, try again.', category='error')

        except Exception as e:
            flash(f'Error checking manager PIN: {e}', category='error')

        try:
            # Check employee PIN
            cur.execute("SELECT pin, is_manager FROM Employees WHERE pin = %s", (entered_pin,))
            result = cur.fetchone()

            if result:
                pin, is_manager = result
                if not is_manager:
                    flash('Login successful as Employee!', category='success')
                    return render_template("pos.html")
                else:
                    flash('Invalid pin for Employee, try again.', category='error')

        except Exception as e:
            flash(f'Error checking employee PIN: {e}', category='error')

        finally:
            cur.close()
            menu_db.close()

    return render_template("login.html", boolean=True)

@auth.route('/order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        try:
            order_items = request.form.getlist('order_item')

            for item in order_items:
                name, category, price = item.split('|')
                cur.execute("INSERT INTO orders (item_name, category, price) VALUES (%s, %s, %s)",
                            (name, category, price))

            menu_db.commit()
            flash('Order Placed Successfully!', category='success')

        except Exception as e:
            flash(f'Error placing order: {e}', category='error')

    return render_template('order.html', apps=apps, entrees=entrees, sides=sides, drinks=drinks)

@auth.route('/Addemp', methods=['GET', 'POST']) #Add Employee 
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
                
                cur.execute("INSERT INTO Employees (firstname, lastname, pin) VALUES (%s, %s, %s)",
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
        # Check if the employee is a manager
        cur.execute("SELECT is_manager FROM Employees WHERE employeeID = %s", (employee_id_to_remove,))
        result = cur.fetchone()

        if result:
            is_manager = result[0]

            if is_manager:
                flash('Manager cannot be removed.', category='error')
            else:
                # Delete the employee if not a manager
                cur.execute("DELETE FROM Employees WHERE employeeID = %s", (employee_id_to_remove,))
                menu_db.commit()
                flash('Employee Removed!', category='success')
        else:
            flash('Employee not found.', category='error')

    except Exception as e:
        flash(f'Error removing employee: {e}', category='error')

@auth.route('/remove_employee', methods=['GET', 'POST'])
def remove_employee_route():
    if request.method == 'POST':
        employee_id_to_remove = int(request.form.get('remove_employee_id'))
        remove_employee(employee_id_to_remove)

    # Fetch the updated employee list after removal
    cur.execute("SELECT * FROM employees")
    employee_list = cur.fetchall()

    return render_template('RemEmp.html', employee_list=employee_list)
