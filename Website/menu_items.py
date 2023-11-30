# from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from bs4 import BeautifulSoup
from Website.db_connector import menu_db as db_connect
from Website.db_connector import mycursor as my_sql_cursor
import os

# Set the working directory to the directory containing the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

my_sql_cursor.execute('''
CREATE TABLE IF NOT EXISTS Menu_Items (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    MenuPrice DECIMAL(3,2)
)
''')

# Commit the table creation
db_connect.commit()

# Menu item data
entree_list = ["Jumbo Dog", "Bacon Burger", "Original Burger", "Fried Chicken", "pasta"]
sides_list = ["Curly Fries", "Onion Rings", "Tater Tots"]
starters_list = ["Fried Calamari", "Fried Mozzerella", "Garlic Bread"]
drinks_list = ["Dark Beer", "Light Beer", "Hard Apple Cider", "Lemonade"]

# SQL function to insert menu items
def sql_menu_insert(Category, items_list):
    for element in items_list:
        my_sql_cursor.execute(f"INSERT INTO Menu_Items (ItemName, Category) VALUES ('{element}', '{Category}')")

# SQL function to update menu items
def sql_menu_update(Category, items_list):
    for i, element in enumerate(items_list, start=1):
        my_sql_cursor.execute(f"UPDATE Menu_Items SET ItemName = '{element}' WHERE ID = {i} AND Category = '{Category}'")
        db_connect.commit()

# Call functions to insert and update menu items
sql_menu_insert("Entrees", entree_list)
sql_menu_update("Sides", sides_list)
sql_menu_update("Appetizers", starters_list)
sql_menu_update("Drinks", drinks_list)

# HTML modification function (assuming the file paths are correct)
def add_to_menu(item_list, item_id):
    menu_dropdown = soup.find(attrs={'id': f'{item_id}'})
    for item_el in item_list:
        new_item = soup.new_tag("a", class_="dropdown-item", href="#")
        menu_dropdown.append(new_item)
        new_item.string = f"{item_el}"

# File paths
menu_fp2 = "templates/menu_add.html"

# Read HTML file
with open(menu_fp2, "r", encoding="utf8") as menu_page:
    soup = BeautifulSoup(menu_page, "html.parser")

# Add menu items to HTML
add_to_menu(entree_list, "entrees")
add_to_menu(sides_list, "sides")
add_to_menu(starters_list, "starters")
add_to_menu(drinks_list, "drinks")

# Remove class attribute
for tag in soup.find_all(attrs={'class_': True}):
    tag['class'] = tag['class_']
    del tag['class_']

# Write the modified HTML back
with open(menu_fp2, "w", encoding="utf8") as updated_menu:
    updated_menu.write(str(soup.prettify()))




 


 
   


  


    

   