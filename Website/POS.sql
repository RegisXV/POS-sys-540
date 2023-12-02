create DATABASE POS;
USE POS;
drop database POS;

Create Table pos (
orderid int primary key auto_increment not null,
employeeID int not null,
ordername varchar(100),
itemID int not null,
cart varchar(100),
cost double,
totalcost double);

Create Table orderlist (
listid int primary key auto_increment not null,
orderid int,
ordername varchar(100) Not NULL,
employeeID int Not NUll,
Foreign Key (employeeID) References Employees(employeeID),
Foreign Key (orderid) References pos (orderid));

Create Table orderhistory(
historyid int primary key auto_increment Not NUll,
orderid int not null,
employeeID int not null,
ordername varchar(100) Not NUll,
total double,
Foreign key (employeeID) References Employees(employeeID),
Foreign Key (orderid) References pos (orderid));

CREATE TABLE Itemlist  (
itemID int primary key NOT NULL,
itemname varchar(100) NOT NULL,
category varchar(255) not Null,
cost int NOT NULL);

CREATE TABLE Employees (
employeeID int primary key auto_increment,
is_manager boolean not null default 0,
firstname varchar(60) NOT NULL,
lastname varchar(60)  NOT NULL,
pin VARCHAR (50) NOT NULL
 );
 insert into Employees(is_manager,firstname,lastname,PIN)
 Values (1,'Joe','Bob','0001');
 select*from Employees;
 
 CREATE TABLE Employee_Salary (
firstname varchar(60),
lastname varchar(60), 
baseSalary int NOT NULL,
tips int NOT NULL,
total_pay int
 );
 






