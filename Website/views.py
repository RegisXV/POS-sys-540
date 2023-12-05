from flask import Blueprint, render_template
#from Website.menu_items import sql_menu_update


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/pos')
def pos():
    return render_template("pos.html")

# @views.route('/menu')
# def menu_view():
#     # bar_menu_update()
#     return render_template("menu.html")

