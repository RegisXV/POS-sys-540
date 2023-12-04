from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from flask_login import login_required
#from Website.menu_items import sql_menu_update 
import re
import mysql.connector

#Connecting Database
menu_db = mysql.connector.connect(
host="localhost",
user="root",
passwd="root",
database="POS",
auth_plugin="mysql_native_password"
)
cur = menu_db.cursor(buffered=True)


auth = Blueprint('auth', __name__)

def get_current_employee_id():
    return session.get('employeeID', None)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    entered_pin = request.form.get('pin')

    if request.method == 'POST':
        try:
            # Check manager PIN
            cur.execute("SELECT employeeID, is_manager FROM Employees WHERE pin = %s", (entered_pin,))
            result = cur.fetchone()

            if result:
                    employeeID, is_manager = result
                    session['employeeID'] = employeeID  # Store employeeID in the session

                    if is_manager:
                        flash('Login successful as Manager!', category='success')
                        return render_template("Manager.html")
                    else:
                        flash('Login successful as Employee!', category='success')
                        return redirect(url_for('auth.create_order'))
                        
        except Exception as e:
            flash(f'Error fetching orders: {e}', category='error')
    return render_template("login.html", boolean=True)

@auth.route('/portal', methods=['GET','POST'])
def portal():

                    # if request.method == 'GET':
                    #     try:
                    #         employeeID = get_current_employee_id()
                    #         cur.execute("SELECT listid, ordername FROM orderlist WHERE employeeID = %s", (employeeID,))
                    #         orders = cur.fetchall()
                    #         print(orders)
                    #         return render_template('orders.html', orders=orders)
                    #     except Exception as e:
                    #         flash(f'Error fetching orders: {e}', category='error')
                    return render_template("orders.html")


@auth.route('/order', methods=['GET', 'POST'])
def create_order():
    # Fetch the list of orders for the current employee
    if request.method == 'GET':
        try:
            employeeID = get_current_employee_id()
            cur.execute("SELECT listid, ordername FROM orderlist WHERE employeeID = %s", (employeeID,))
            orders = cur.fetchall()
            print(orders)
            return render_template('orders.html', orders=orders)
        except Exception as e:
            flash(f'Error fetching orders: {e}', category='error')

    if request.method == 'POST':
        try:
            employeeID = get_current_employee_id() 
            ordername = request.form.get('ordername')
            orders = cur.fetchall()
            cur.execute("INSERT INTO orderlist (ordername, employeeID) VALUES (%s, %s)", (ordername, employeeID))
            last_listID = cur.lastrowid
            print(last_listID)
            cur.execute(f"CREATE TABLE IF NOT EXISTS {ordername}_{last_listID} (orderID int auto_increment primary key,\
                employeeID int,listID int, ordername VARCHAR(255),ItemID int,Item_name VARCHAR(255),cost double,quantity int,\
                    foreign key (employeeID) References Employees(employeeID),\
                        foreign key (listID) References orderlist(listid),\
                            foreign key (ItemID) References Itemlist(itemID))")
            cur.execute("Select Last_Insert_ID()")
            last_orderid = cur.fetchone()[0]
            print(last_orderid)
            cur.execute("Update orderlist set orderid=%s where listid=%s",(last_orderid,last_listID))
            print(last_orderid)
            cur.execute(f"Insert into {ordername}_{last_listID}(ordername,employeeID,listID) Values (%s,%s,%s)",(ordername, employeeID, last_listID))
            cur.execute("Insert into pos(orderid,employeeID,ordername) Values (%s,%s,%s)",(last_orderid,employeeID,ordername))
            cur.execute("Select Last_Insert_ID()")
            last_posid = cur.fetchone()[0]
            cur.execute("Update orderlist set posid=%s where listid=%s",(last_posid,last_listID))
            menu_db.commit()
            flash('Order Placed Successfully!', category='success')
            
            # Redirect to the orders page after placing the order
            return redirect(url_for('auth.create_order'))
         
        except Exception as e:
            flash(f'Error placing order: {e}', category='error')

    cur.close()
    return render_template('orders.html', orders=[])
       




def fetch_menu_items_by_category(category):
    cur.execute("SELECT itemname, cost FROM Itemlist WHERE category = %s", (category,))
    menu_items = cur.fetchall()

    cur.close()

    return menu_items

@auth.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        try:
            employeeID = int(request.form.get('employeeID'))
            ordername = request.form.get('ordername')
            
            # Retrieve selected items from the checkbox values
            order_items = request.form.getlist('order_item')
            
            # Process the order items as needed (e.g., save to the database)
            
            flash('Order Placed Successfully!', category='success')
            return redirect('pos.html')
        except Exception as e:
            flash(f'Error placing order: {e}', category='error')


    apps = fetch_menu_items_by_category('apps')
    
    
    cur.close()
    return render_template('pos.html', apps=apps)

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
    cur.execute("SELECT firstname,lastname,pin FROM employees")
    employee_list = cur.fetchall()

    return render_template('RemEmp.html', employee_list=employee_list)

@auth.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    flash('Logout successful!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/history')
def order_history():

    return render_template('orderhistory.html')