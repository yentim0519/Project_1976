CREATE TABLE perfume_data(
id INT NOT NULL AUTO_INCREMENT,
product_brand VARCHAR(100),
product_name VARCHAR(100),
fragrance_notes VARCHAR(50),
top_notes VARCHAR(50),
middle_notes VARCHAR(50),
base_notes VARCHAR(50),
product_url VARCHAR(100),
PRIMARY KEY(ID)
)

ALTER TABLE perfume_data CONVERT TO CHARACTER SET UTF8