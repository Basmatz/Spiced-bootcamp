create table shippers
(
	"shipperID" integer not null
		constraint shippers_pk
			primary key,
	"companyName" varchar(100),
	phone varchar(100)
);

alter table shippers owner to postgres;

create unique index shippers_shipperid_uindex
	on shippers ("shipperID");

create table categories
(
	"categoryID" integer not null
		constraint categories_pk
			primary key,
	"categoryName" varchar(100),
	description varchar(100),
	picture text
);

alter table categories owner to postgres;

create unique index categories_categoryid_uindex
	on categories ("categoryID");

create table customers
(
	"customerID" varchar(5) not null
		constraint customers_pk
			primary key,
	"companyName" varchar(100),
	"contactName" varchar(100),
	"contactTitle" varchar(100),
	address varchar(100),
	city varchar(100),
	region varchar(100),
	"postalCode" varchar(100),
	country varchar(100),
	phone varchar(100),
	fax varchar(100)
);

alter table customers owner to postgres;

create unique index customers_customerid_uindex
	on customers ("customerID");

create table employees
(
	"employeeID" integer not null
		constraint employees_pk
			primary key,
	"lastName" varchar(100),
	"firstName" varchar(100),
	title varchar(100),
	"titleOfCourtesy" varchar(100),
	"birthDate" timestamp,
	"hireDate" timestamp,
	address varchar(100),
	city varchar(100),
	region varchar(100),
	"postalCode" varchar(100),
	country varchar(100),
	"homePhone" varchar(100),
	extension integer,
	photo text,
	notes text,
	"reportsTo" varchar(100),
	"photoPath" text
);

alter table employees owner to postgres;

create table employee_territories
(
	"employeeID" integer
		constraint employee_territories_employees_employeeid_fk
			references employees,
	"territoryID" integer not null
		constraint employee_territories_pk
			primary key
);

alter table employee_territories owner to postgres;

create unique index employee_territories_territoryid_uindex
	on employee_territories ("territoryID");

create unique index employees_employeeid_uindex
	on employees ("employeeID");

create table order_details
(
	"orderID" integer,
	"productID" integer,
	"unitPrice" numeric,
	quantity integer,
	discount numeric,
	"keyID" serial not null
		constraint order_details_pk
			primary key
);

alter table order_details owner to postgres;

create unique index order_details_keyid_uindex
	on order_details ("keyID");

create table orders
(
	"orderID" integer not null
		constraint orders_pk
			primary key,
	"customerID" varchar(100),
	"employeeID" integer,
	"orderDate" timestamp,
	"requiredDate" timestamp,
	"shippedDate" timestamp,
	"shipVia" integer,
	freight numeric,
	"shipName" varchar(100),
	"shipAddress" varchar(100),
	"shipCity" varchar(100),
	"shipRegion" varchar(100),
	"shipPostalCode" varchar(100),
	"shipCountry" varchar(100)
);

alter table orders owner to postgres;

create unique index orders_orderid_uindex
	on orders ("orderID");

create table products
(
	"productID" integer not null
		constraint products_pk
			primary key,
	"productName" varchar(100),
	"supplierID" integer,
	"categoryID" integer,
	"quantityPerUnit" varchar(100),
	"unitPrice" numeric,
	"unitsInStock" integer,
	"unitsOnOrder" integer,
	"reorderLevel" integer,
	discontinued integer
);

alter table products owner to postgres;

create unique index products_productid_uindex
	on products ("productID");

create table regions
(
	"regionID" integer not null
		constraint regions_pk
			primary key,
	"regionDescription" varchar(100)
);

alter table regions owner to postgres;

create unique index regions_regionid_uindex
	on regions ("regionID");

create table suppliers
(
	"supplierID" integer not null
		constraint suppliers_pk
			primary key,
	"companyName" varchar(100),
	"contactName" varchar(100),
	"contactTitle" varchar(100),
	address varchar(100),
	city varchar(100),
	region varchar(100),
	"postalCode" varchar(100),
	country varchar(100),
	phone varchar(100),
	fax varchar(100),
	"homePage" text
);

alter table suppliers owner to postgres;

create unique index suppliers_supplierid_uindex
	on suppliers ("supplierID");

create table territories
(
	"territoryID" integer not null
		constraint territories_pk
			primary key,
	"territoryDescription" text,
	"regionID" integer
);

alter table territories owner to postgres;

create unique index territories_territoryid_uindex
	on territories ("territoryID");

