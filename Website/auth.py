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
            else:
                flash('Invalid pin please try again', category='error')
                        
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
            cur.execute("Select is_manager from employees where employeeID = %s", (employeeID,))
            result = cur.fetchall()
            if result:
                isman = int(result[0][0])
                if isman == 1:
                    cur.execute("SELECT listid, ordername FROM orderlist")
                    orders = cur.fetchall()
                    return render_template('orders.html', orders=orders)
                else:
                    cur.execute("SELECT listid, ordername FROM orderlist WHERE employeeID = %s", (employeeID,))
                    orders = cur.fetchall()
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
            cur.execute(f"CREATE TABLE IF NOT EXISTS {ordername}_{last_listID} (orderID int auto_increment primary key, posid int,\
                employeeID int,listID int, ordername VARCHAR(255),ItemID int,Item_name VARCHAR(255),cost double,quantity int,\
                    foreign key (employeeID) References Employees(employeeID),\
                        foreign key (listID) References orderlist(listid),\
                            foreign key (ItemID) References Itemlist(itemID))")
            cur.execute("Select Last_Insert_ID()")
            last_orderid = cur.fetchone()[0]
            cur.execute("Update orderlist set orderid=%s where listid=%s",(last_orderid,last_listID))
            cur.execute(f"Insert into {ordername}_{last_listID}(ordername,employeeID,listID) Values (%s,%s,%s)",(ordername, employeeID, last_listID))
            cur.execute("Insert into pos(listid,employeeID,ordername) Values (%s,%s,%s)",(last_listID,employeeID,ordername))
            cur.execute("Select Last_Insert_ID()")
            last_posid = cur.fetchone()[0]
            cur.execute("Update orderlist set posid=%s where listid=%s",(last_posid,last_listID))
            cur.execute(f"Update {ordername}_{last_listID} set posid=%s where listid=%s", (last_posid,last_listID))
            menu_db.commit()
            flash('Order Placed Successfully!', category='success')
            
            # Redirect to the orders page after placing the order
            return redirect(url_for('auth.create_order'))
         
        except Exception as e:
            flash(f'Error placing order: {e}', category='error')

    cur.close()
    return render_template('orders.html', orders=[])
       
@auth.route('/menu') #Leave for possible changes later but this is not the actual fetch menu items
def fetch_menu_items(orderid,ordername):
    try:
        cur.execute (f"Select posid, employeeID, ordername, listID from {ordername}_{orderid} ")
        details = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'apps' ", )
        apps = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'entrees' ", )
        entrees = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'sides' ", )
        sides = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'drinks' ", )
        drinks = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'desserts' ", )
        desserts = cur.fetchall()
        print(details,apps,entrees,sides,drinks,desserts)
        return render_template('pos2.html', details=details, apps=apps, entrees=entrees, sides=sides, drinks=drinks, desserts=desserts)
    except Exception as e:
    
        flash(f'Error fetching menu items: {e}', category='error')
        return redirect(url_for('auth.create_order'))

    
@auth.route('/menu')
def fetch_menu_items():
    cur.execute ("if exists select * from ")

    cur.execute("SELECT DISTINCT category FROM itemlist")

    itemandcat = {}

    category_list = cur.fetchall()

    cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'apps' ", )
    apps = cur.fetchall()
    print(apps)
    cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'entrees' ", )
    entrees = cur.fetchall()
    print(entrees)
    cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'sides' ", )
    sides = cur.fetchall()
    cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'drinks' ", )
    drinks = cur.fetchall()
    cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'desserts' ", )
    desserts = cur.fetchall()
    cur.close()
    return render_template('pos2.html', apps=apps, entrees=entrees, sides=sides, drinks=drinks, desserts=desserts)
    


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
    return render_template("AddEmp.html")

def remove_employee(empid,manager):
    try:    
        if manager==1:
                flash('Manager cannot be removed.', category='error')
        else:
                # Delete the employee if not a manager
                cur.execute("DELETE FROM Employees WHERE employeeID = %s", (empid,))
                menu_db.commit()
                flash('Employee Removed!', category='success')

    except Exception as e:
        flash(f'Error removing employee: {e}', category='error')

@auth.route('/remove_employee', methods=['GET', 'POST'])
def remove_employee_route():
    try:
        cur.execute("SELECT * FROM employees")
        employee_list = cur.fetchall()
        
        if request.method == 'POST':
            empid = request.form.get("EmpID")
            manager = int(request.form.get("isman"))
            remove_employee(empid,manager)
            return redirect(url_for('auth.remove_employee_route'))

        # Fetch the updated employee list after removal
        

        return render_template('RemEmp.html', employee_list=employee_list)
    except Exception as e:
        flash(f'Error listing employees: {e}', category='error')

@auth.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    flash('Logout successful!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/history')
def order_history():
    cur.execute("SELECT * from orderhistory" )
    history = cur.fetchall()

    return render_template('orderhistory.html',history=history)

@auth.route('/delete_order', methods=['POST'])
def delete_order():
    try:
        order_id = request.form.get('order_id')
        order_name = request.form.get('order_name')  

        cur.execute("START TRANSACTION") #In case things go wrong

        cur.execute(f"DELETE FROM {order_name}_{order_id} WHERE listID = %s", (order_id,))
        cur.execute("DELETE FROM orderlist WHERE listid = %s", (order_id,))
        cur.execute("DELETE FROM pos WHERE listid = %s", (order_id,))
       

        cur.execute(f"Drop Table {order_name}_{order_id}")

        cur.execute("COMMIT")

        
        flash('Order deleted', category='success')
        return redirect(url_for('auth.create_order'))

    except Exception as e:
        menu_db.rollback()
        flash(f'Error deleting order: {e}', category='error')
        return redirect(url_for('auth.create_order'))

@auth.route('/access_order', methods=['POST'])
def access_order():
    try:    
        if request.method == 'POST':
            itemid = request.form.get('itemid')
            itemname=request.form.get('itemname')
            itemcost=request.form.get('cost')
            add_to_cart(orderid,ordername,itemid,itemname,itemcost)
            print(orderid,ordername,itemid,itemname,itemcost) 
        orderid = request.form.get('order_id')
        ordername = request.form.get('order_name')
        details, apps, entrees, sides, drinks, desserts = fetch_menu_items1(orderid, ordername)
        return render_template('pos2.html', details=details, apps=apps, entrees=entrees, sides=sides, drinks=drinks, desserts=desserts)
        
       
    
        
    except Exception as e:
        flash(f'Error accessing order: {e}', category='error')
        return redirect(url_for('auth.create_order'))
    
def fetch_menu_items1(orderid,ordername):
    try:
        cur.execute (f"Select posid, employeeID, ordername, listID from {ordername}_{orderid} ")
        details = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'apps' ", )
        apps = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'entrees' ", )
        entrees = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'sides' ", )
        sides = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'drinks' ", )
        drinks = cur.fetchall()
        cur.execute("SELECT itemID, itemname, cost FROM Itemlist WHERE category = 'desserts' ", )
        desserts = cur.fetchall()
        return (details, apps, entrees, sides, drinks, desserts)
    except Exception as e:
    
        flash(f'Error fetching menu items: {e}', category='error')
        return redirect(url_for('auth.create_order'))

def Add_to_cart(orderid,ordername,cost,quantity):

        menuItems = fetch_menu_items1()

        cur.execute("SELECT posid, employeeID, ordername, listID FROM order_table WHERE order_id = %s", (orderid,))
        order_data = cur.fetchone()
                    
        cur.execute(
            "INSERT INTO {ordername}_{orderid}(order_id, item_name, cost, quantity) VALUES (%s, %s, %s, %s)",
            (orderid, ordername, cost, quantity)
        )