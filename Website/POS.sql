create DATABASE POS;
USE POS;

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

select * from Itemlist;
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
 
Create Table pos (
posid int primary key auto_increment not null,
listid int,
employeeID int not null,
ordername varchar(100),
totalcost double not null default 0);
select*from pos;

Create Table orderlist (
listid int primary key auto_increment not null,
orderid int,
ordername varchar(100) Not NULL,
posid int,
employeeID int Not NUll,
Foreign Key (employeeID) References Employees(employeeID),
Foreign Key (posid) References pos (posid));



Create Table orderhistory(
historyid int primary key auto_increment Not NUll,
posID int not null,
employeeID int not null,
ordername varchar(100) Not NUll,
total double not null default 0,
ispaid boolean default 0);


-- Triggers this works with the current delete procedure 
DELIMITER //
CREATE TRIGGER trg_delete_pos_and_insert_orderhistory
BEFORE DELETE ON pos
FOR EACH ROW
BEGIN
	INSERT INTO orderhistory (posid, employeeID, ordername,  total)
    VALUES (OLD.posid, OLD.employeeID, OLD.ordername,  OLD.totalcost);
END;
//
DELIMITER ;

 -- test for delete procedure
 start transaction;
 select*from Josh_1;
 delete from Josh_1 where listID=1;
 select*from Josh_1;
 select*from orderlist;
 delete from orderlist where posid=1;
 select * from pos;
 delete from pos where posid=1;
 select*from pos;
 select* from orderlist;
 select*from orderhistory;
 rollback;
 drop table Josh_1;
 


ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'root';

Drop database pos;

select*from John_1;
select*from pos;
select*from orderlist;
select*from orderhistory;

drop table orderhistory;


