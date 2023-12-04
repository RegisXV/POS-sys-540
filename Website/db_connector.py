import mysql.connector


menu_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="POS"
)

mycursor = menu_db.cursor()
