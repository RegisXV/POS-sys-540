from flask import current_app
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

def create_tables():
    mysql = current_app.mysql
    try:
        mysql.connection.ping()
    except Exception as e:
        return 
    with current_app.app_context():
        cur = mysql.connection.cursor()
        cur.close()
        mysql.connection.commit()