# from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, current_app
from bs4 import BeautifulSoup



#iterate through mysql table cells instead of lists
entree_list=["Jumbo Dog","Bacon Burger","Original Burger"]
sides_list=["Curly Fries","Onion Rings","Tater Tots"]
starters_list=["Fried Calamari","Fried Mozzerella","Garlic Bread"]
drinks_list=["Dark Beer","Light Beer","Hard Apple Cider","Lemonade"]



def add_to_menu(item_el,item_list,item_id):
 menu_dropdown = soup.find(attrs={'id':f'{item_id}'})

 for item_el in item_list:
  new_item = soup.new_tag("a",class_="dropdown-item",href="#")
  if item_el not in str(new_item):
   menu_dropdown.append(new_item)
   new_item.string=f"{item_el}"
  
  
#replace with full host filepath.  Run html in browser from file explorer, copy path from browser
menu_fp = "C:/Users/Austin/Downloads/CSC_540/Team_Project/POS-sys-540/Website/templates/menu.html"

#replace with full host filepath.  Run html in browser from file explorer, copy path from browser
with open (menu_fp, "r", encoding="utf8") as menu_page:

 soup = BeautifulSoup(menu_page, "html.parser")

 add_to_menu("entree",entree_list,"entrees")
 add_to_menu("sides",sides_list,"sides")
 add_to_menu("starters",starters_list,"starters")
 add_to_menu("drinks",drinks_list,"drinks")
 
 for tag in soup.find_all(attrs={'class_': True}):
  tag['class'] = tag['class_']
  del tag['class_']
 

with open(menu_fp, "w", encoding="utf8") as updated_menu:
 
 updated_menu.write(str(soup.prettify()))

# return render_template("menu.html")

 


 
   


  


    

   