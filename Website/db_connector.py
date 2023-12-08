import mysql.connector


menu_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="POS",
  auth_plugin='mysql_native_password'
)

mycursor = menu_db.cursor()

emptydict: {}

mycursor.execute("CALL itemSelection(@ItemNameItemCat);")
mycursor.execute("SELECT @ItemNameItemCat;")

for cur in mycursor:
  print(cur)



