create DATABASE POS;
USE POS;
drop database POS;

Create Table pos (
posid int primary key auto_increment not null,
orderid int,
employeeID int not null,
ordername varchar(100),
totalcost double);
select*from pos;

Create Table orderlist (
listid int primary key auto_increment not null,
orderid int,
ordername varchar(100) Not NULL,
posid int,
employeeID int Not NUll,
Foreign Key (employeeID) References Employees(employeeID),
Foreign Key (posid) References pos (posid));

select * from orderlist;

select * from Jack_2;

Create Table orderhistory(
historyid int primary key auto_increment Not NUll,
orderid int not null,
employeeID int not null,
ordername varchar(100) Not NUll,
total double,
Foreign key (employeeID) References Employees(employeeID),
Foreign Key (orderid) References pos (orderid));

CREATE TABLE Itemlist  (
itemID int primary key auto_increment NOT NULL,
itemname varchar(100) NOT NULL,
category varchar(255) not Null,
cost double NOT NULL);


Insert into Itemlist(itemname,category,cost) 
Values ("Sonic's chilli cheese dogs",'entrees',7.99),
('House of the DragonBurger','entrees',6.99),
("Dracula's Steak and Cheese",'entrees',6.50),
("Rock n' Roll Chicken Sandwhich",'entrees',8.75),
("Kyle's Fav Ham and Cheese",'entrees',10.00),
('Angel wings','apps',5.00),
('Ew Nachos','apps',15.00),
('Scooby doo dog','apps',4.00),
('The Bowling for soup','apps',6.50),
("Papa John's mac and cheese bites",'apps',4.50),
('The Big Fry','sides',2.50),
('the small fry','sides',2.00),
('The One ring','sides',2.50),
('the small ring','sides',2.00),
('Totters','sides',3.00),
('routebeer','drinks',1.00),
("Mcdonald's Coke",'drinks',1.15),
("What you don't like tap waterbottle",'drinks',2.00),
('Spritsy Sprite','drinks',1.50),
("Sherly's Temple of Doom", 'drinks',3.50),
('Poptart','desserts',1.00),
('The Chocolate Volcano','desserts',5.00),
('Big ole Twinky','desserts',2.00),
('One scoop of icecream','desserts',1.50),
('How about two scoops of icecream','desserts',3.00);


CREATE TABLE Employees (
employeeID int primary key auto_increment,
is_manager boolean not null default 0,
firstname varchar(60) NOT NULL,
lastname varchar(60)  NOT NULL,
pin VARCHAR (50) NOT NULL
 );
 insert into Employees(is_manager,firstname,lastname,PIN)
 Values (1,'Joe','Bob','0001');
 select * from Employees;

 
 CREATE TABLE Employee_Salary (
firstname varchar(60),
lastname varchar(60), 
baseSalary int NOT NULL,
tips int NOT NULL,
total_pay int
 );
 
select * from J_7;
select*from Itsalive_10;
 
 
 
select*from Letsgo_11;

select*from Ara_16;



-- Triggers 
DELIMITER //
CREATE TRIGGER trg_insert_orderlist
AFTER INSERT ON pos
FOR EACH ROW
BEGIN
    INSERT INTO orderlist (orderid, ordername, employeeID)
    VALUES (NEW.orderid, NEW.ordername, NEW.employeeID);
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_delete_orderlist_and_insert_orderhistory
BEFORE DELETE ON pos
FOR EACH ROW
BEGIN

    INSERT INTO orderhistory (orderid, ordername, employeeID, total)
    VALUES (OLD.orderid, OLD.ordername, OLD.employeeID, OLD.totalcost);
    DELETE FROM orderlist WHERE orderid = OLD.orderid;
END;
//
DELIMITER ;

ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'root';
