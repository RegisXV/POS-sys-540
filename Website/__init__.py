from flask import Flask
from flask_mysqldb import MySQL
def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'your secret key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'OogaBooga619'
    app.config['MYSQL_DB'] = 'POS'

    
    mysql = MySQL(app)
    print(mysql)
    from .models import create_tables

    app.mysql = mysql
    with app.app_context():
        create_tables()


    # Ensure tables are created when the app starts
    with app.app_context():
        from .models import create_tables
        create_tables()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app