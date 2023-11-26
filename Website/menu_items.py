# from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from bs4 import BeautifulSoup
from Website.db_connector import menu_db as db_connect
from Website.db_connector import mycursor as my_sql_cursor


#iterate through mysql table cells instead of lists
entree_list=["Jumbo Dog","Bacon Burger","Original Burger","Fried Chicken","pasta"]
sides_list=["Curly Fries","Onion Rings","Tater Tots"]
starters_list=["Fried Calamari","Fried Mozzerella","Garlic Bread"]
drinks_list=["Dark Beer","Light Beer","Hard Apple Cider","Lemonade"]


def sql_menu_insert(Category,items_list):
  for element in items_list:
    my_sql_cursor.execute(f"INSERT INTO Menu_Items ({Category}) SELECT  VALUES ('{element}')")
    

def sql_menu_update(col_name,items_list):
  i = 1
  for element in items_list:
    my_sql_cursor.execute(f"UPDATE Menu_Items SET {col_name} = '{element}' WHERE ID = {i}")
    db_connect.commit()
    i += 1
 
sql_menu_insert("Entrees",entree_list)
sql_menu_update("Sides", sides_list)
sql_menu_update("Appetizers",starters_list)
sql_menu_update("Drinks", drinks_list)

def bar_menu_update():
  def add_to_menu(item_list,item_id):
    menu_dropdown = soup.find(attrs={'id':f'{item_id}'})

    for item_el in item_list:
      new_item = soup.new_tag("a",class_="dropdown-item",href="#")
      

      if item_el in item_list:
        menu_dropdown.append(new_item)
        new_item.string=f"{item_el}"
      else:
        del item_el
        
  
  
#replace with full host filepath.  Run html in browser from file explorer, copy path from browser
  menu_fp = "C:/Users/Austin/Downloads/CSC_540/Team_Project/POS-sys-540/Website/templates/menu.html"
  menu_fp2 = "C:/Users/Austin/Downloads/CSC_540/Team_Project/POS-sys-540/Website/templates/menu_add.html"

#replace with full host filepath.  Run html in browser from file explorer, copy path from browser
  with open (menu_fp2, "r", encoding="utf8") as menu_page:

    soup = BeautifulSoup(menu_page, "html.parser")

    add_to_menu(entree_list,"entrees")
    add_to_menu(sides_list,"sides")
    add_to_menu(starters_list,"starters")
    add_to_menu(drinks_list,"drinks")
 
    for tag in soup.find_all(attrs={'class_': True}):
      tag['class'] = tag['class_']
      del tag['class_']
 

  with open(menu_fp2, "w", encoding="utf8") as updated_menu:
 
    updated_menu.write(str(soup.prettify()))





 


 
   


  


    

   