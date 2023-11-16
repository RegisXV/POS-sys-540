from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        cur = current_app.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE pin = %s", (pin,))
        user = cur.fetchone()
        cur.close()

        if user:
            # User found, do something
            flash('Login successful!', category='success')
        else:
            flash('Invalid pin, try again.', category='error')

    return render_template("login.html", boolean=True)

@auth.route('/manager', methods=['GET', 'POST'])
def manager():
    return render_template("Manager.html")

@auth.route('/Addemp', methods=['GET', 'POST'])
def addemp():
    if request.method == 'POST':
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        pin1 = request.form.get('Pin1')
        pin2 = request.form.get('Pin2')

        if len(fname) == 0:
            flash('Insert valid first name', category='error')
        elif len(lname) == 0:
            flash('Insert valid last name', category='error')
        elif pin1 == 0:
            flash('Insert valid pin', category='error')
        elif pin1 != pin2:
            flash('Pins do not match', category='error')
        else:
            try:
                mysql = current_app.mysql  # Access mysql object from current_app
                cur = mysql.connection.cursor()

                # Insert employee data into the 'employees' table (replace with your actual table name)
                cur.execute("INSERT INTO employees (firstname, lastname, pin) VALUES (%s, %s, %s)",
                            (fname, lname, pin1))

                mysql.connection.commit()
                cur.close()

                flash('Employee Added!', category='success')
            except Exception as e:
                flash(f'Error adding employee: {e}', category='error')

    return render_template("AddEmp.html")


