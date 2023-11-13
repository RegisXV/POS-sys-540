Create Database POS;
use POS;
Create table manager(id INT AUTO_INCREMENT,
firstname char (255),
lastname char(255),
pin Varchar(255) Primary Key,
Foreign Key (id) References employees(employee_id));

drop table manager;
Insert into manager(firstname,lastname,pin)
Values('Joe','Bob','0001');

Select* from manager;

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    pin VARCHAR(255) NOT NULL
);
Insert into employees(firstname,lastname,pin)
Values('Joe','Bob','0001');
drop table employees;

