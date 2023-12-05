from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
import os
import ast
from bs4 import BeautifulSoup
import mysql.connector
from icecream import ic
# from Website.auth import cur 
# from Website.auth import cur

# Set the working directory to the directory containing the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

menu_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="POS"
)

cur = menu_db.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS Menu_Items (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    MenuPrice DECIMAL(6,2)
)
""")

# Commit the table creation
menu_db.commit()

# Menu item data


def existing_items():
    total_list = []
    proc_exists_check =  "DROP PROCEDURE IF EXISTS value_match;"
    existing_items_proc =  """
    CREATE PROCEDURE value_match (
    INOUT items_array TEXT)
    BEGIN
    DECLARE done BOOL DEFAULT false;
    DECLARE Items VARCHAR(80) DEFAULT "";

    DECLARE value_cur CURSOR FOR SELECT ItemName FROM Itemlist;
    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET done = true;

    OPEN value_cur;

    SET items_array = '';

    Values_loop: LOOP

    FETCH value_cur INTO Items;

        IF done = true THEN
            LEAVE Values_loop;
        END IF;
        SET items_array = Concat("'", Items, "'", ",", items_array);
    END LOOP;
    CLOSE value_cur;
    END

        """
    cur.execute(proc_exists_check )
    cur.execute(existing_items_proc)
    menu_db.commit()
    cur.execute("CALL value_match(@items_array);")
    cur.execute("SELECT @items_array;")
    

    for items_list in cur:
        total_list.append(items_list)
    return total_list
print(existing_items())
 # SQL function to insert menu items
# def sql_menu_insert(Category, items_list):
         
#     for item in items_list:
#         if item not in str(existing_items()):
#             cur.execute(f"INSERT INTO Menu_Items (ItemName, Category, MenuPrice) VALUES ('{item}', '{Category}',{items_list[item]})")
#     menu_db.commit()

# sql_menu_insert("Entrees", entrees_list)
# sql_menu_insert("Sides", sides_list)
# sql_menu_insert("Starters", starters_list)
# sql_menu_insert("Drinks", drinks)


# def add_from_mysql(item_cat):
#     itemsList = []
#     cat_select = (f"SELECT ItemName FROM Menu_Items WHERE Category = '{item_cat}'")
#     cur.execute(cat_select)
   
#     for item in cur:
#         itemsList.append(item)
#     return itemsList      
  

# # HTML modification function (assuming the file paths are correct)
# def add_to_menu_html(item_list, item_id):
#     menu_dropdown = soup.find(attrs={'id': f'{item_id}'})
#     for item_el in item_list:
#         elements = str(item_el).strip("(),'")
#         new_item = soup.new_tag("a", class_="dropdown-item", href="#")
#         menu_dropdown.append(elements)
#         new_item.string = f"{item_el}"

# # File paths
# menu_fp = "templates/menu.html"

# # Read HTML file
# with open(menu_fp, "r", encoding="utf8") as menu_page:
# #with open(menu_fp2, "r", encoding="utf8") as menu_page:
#     soup = BeautifulSoup(menu_page, "html.parser")

# # # Add menu items to HTML


# # Replace "_class" attribute with "class"
# for tag in soup.find_all(attrs={'class_': True}):
#     tag['class'] = tag['class_']
#     del tag['class_']

# # # Write the modified HTML back
# # with open(menu_fp, "w", encoding="utf8") as updated_menu:
# #     updated_menu.write(str(soup.prettify()))




 


 
   


  


    

   