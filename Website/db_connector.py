import mysql.connector


menu_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="POS",
  auth_plugin='mysql_native_password'
)

mycursor = menu_db.cursor()
