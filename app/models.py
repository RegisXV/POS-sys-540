from flask import current_app
from flask_mysqldb import MySQL

def create_users_table():
    # Ensure that the 'mysql' extension is available in the app context
    if 'mysql' not in current_app.extensions:
        raise RuntimeError("MySQL extension not initialized. Call MySQL.init_app(app) first.")

    # Get the MySQL connection
    mysql = current_app.extensions['mysql']

    # Create a cursor to execute SQL queries
    cursor = mysql.connection.cursor()

    # Define the SQL query to create a 'users' table
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
    );
"""

    try:
        # Execute the query to create the 'users' table
        cursor.execute(create_users_table_query)
        # Commit the changes to the database
        mysql.connection.commit()
    except Exception as e:
    # Rollback the changes in case of an error
        mysql.connection.rollback()
        print(f"Error creating tables: {e}")
    finally:
        # Close the cursor
        cursor.close()

