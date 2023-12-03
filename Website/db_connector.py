import mysql.connector


menu_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="POS"
)

mycursor = menu_db.cursor()
