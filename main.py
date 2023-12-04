from Website import create_app
from flask_mysqldb import MySQL

app = create_app()
# mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)
