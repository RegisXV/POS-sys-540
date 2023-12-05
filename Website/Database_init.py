# import mysql.connector
# from mysql.connector import Error
# import os

# def create_database():
#     try:
#         # Get the path to the current script
#         script_dir = os.path.dirname(os.path.abspath(__file__))

        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            auth_plugin='mysql_native_password'
        )
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='root',
#             database="POS"
#         )

#         cursor = connection.cursor()

#         # Check if the database exists
#         cursor.execute("SHOW DATABASES LIKE 'POS'")
#         database_exists = cursor.fetchone()

#         if not database_exists:
#             # Create the database from the SQL file
#             sql_file_path = os.path.join(script_dir, 'POS.sql')
#             with open(sql_file_path, 'r') as sql_file:
#                 sql_script = sql_file.read()
#                 cursor.execute(sql_script)

#         cursor.close()
#         connection.close()

#     except Error as e:
#         print(f"Error: {e}")

# create_database()