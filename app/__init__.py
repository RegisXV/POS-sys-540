from flask import Flask
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

# Load environment variables from .flaskenv
load_dotenv('.env')

IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASSWORD')
DB_NAME = environ.get('DB_NAME')

# Initialize MySQL extension with the Flask app
app.config['MYSQL_HOST'] = IP
app.config['MYSQL_USER'] = USERNAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DB_NAME

mysql = MySQL(app)

with app.app_context():
    models.create_users_table()



from app import models