create DATABASE POS;
USE POS;

CREATE TABLE Menu (
ItemID int primary key,
Itemname varchar(100)
);

CREATE TABLE ItemStock (
ItemID int primary key NOT NULL,
Itemname varchar(100) NOT NULL,
totalQuant int NOT NULL,
ItemCost int NOT NULL);


delimiter //
CREATE TRIGGER receivedItem BEFORE UPDATE on ItemStock
FOR EACH ROW
BEGIN
SET @AddQuant := old.totalQuant + new.totalQuant;
SET @MinusQuant := old.totalQuant - new.TotalQuant;

	IF new.totalQuant >= 0 THEN 
		SET new.totalQuant = @AddQuant;
	ELSEIF new.totalQuant > 0 THEN
		SET new.totalQuant = @MinusQuant;
	ELSE 
		SET new.totalQuant = @addQuant;
	END IF;
END;//
delimiter ;


CREATE TABLE Managers (
ID int auto_increment,
firstname VARCHAR (60) NOT NULL,
lastname VARCHAR (60) NOT NULL,
PIN VARCHAR (50) NOT NULL
);

CREATE TABLE Employees (
employeeID int primary key auto_increment,
firstname varchar(60) NOT NULL,
lastname varchar(60)  NOT NULL,
PIN VARCHAR (50) NOT NULL
 );
 
 CREATE TABLE Employee_Salary (
firstname varchar(60),
lastname varchar(60), 
baseSalary int NOT NULL,
tips int NOT NULL,
total_pay int
 );
 
 #required salary is $25000
delimiter //
CREATE TRIGGER min_server_pay BEFORE UPDATE ON Employee_Salary 
FOR EACH ROW 
BEGIN
	IF new.baseSalary + new.tips < 25000 THEN
		SET new.baseSalary = 25000 - new.tips; 
        SET new.total_pay = new.baseSalary + new.tips;
	END IF;
END;//
delimiter ;
	
CREATE TABLE Sales_Table (
ListID int,
OrderID int,
EmployeeID int,
totalPrice int );



delimiter//
CREATE TRIGGER item_POS_update AFTER INSERT ON POS
FOR EACH ROW
BEGIN 
END;//
delimiter// ;

# will update item quantity in inventory after order has been placed.  Maybe create separate tables for food base price and sale price?





#### Original Code #######


-- Create Database POS;
-- use POS;
-- Create table manager(id INT AUTO_INCREMENT,
-- firstname char (255),
-- lastname char(255),
-- pin Varchar(255) Primary Key,
-- Foreign Key (id) References employees(employee_id));

-- drop table manager;
-- Insert into manager(firstname,lastname,pin)
-- Values('Joe','Bob','0001');

-- Select* from manager;

-- CREATE TABLE employees (
    -- employee_id INT AUTO_INCREMENT PRIMARY KEY,
    -- firstname VARCHAR(255) NOT NULL,
    -- lastname VARCHAR(255) NOT NULL,
    -- pin VARCHAR(255) NOT NULL
-- );
-- Insert into employees(firstname,lastname,pin)
-- Values('Joe','Bob','0001');
-- drop table employees;




