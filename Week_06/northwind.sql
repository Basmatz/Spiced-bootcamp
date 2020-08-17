DROP TABLE IF EXISTS shippers;

CREATE TABLE shippers (
  shipper_id SERIAL,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(15)
);

COPY shippers (shipper_id, company_name, phone)
FROM 'C:\logistic-lemongrass-student-code\Week_06\northwind_data_clean-master\data\shippers.csv'
DELIMITER ','
CSV HEADER;