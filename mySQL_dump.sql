DROP DATABASE IF EXISTS `grocery_store`;
CREATE DATABASE `grocery_store`;
USE `grocery_store`;
SET character_set_client = utf8mb4;


-- --------------------
-- STORE
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`store` (
	`store_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `address_ID` INT,
    `number_of_employees` INT NOT NULL DEFAULT 0,
    `number_of_sales` INT NOT NULL DEFAULT 0,
    `total_revenue` INT NOT NULL DEFAULT 0,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;


-- --------------------
-- PERSONAL INFORMATION
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`personal_information` (
	`personal_information_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `address_ID` INT,
    `name` VARCHAR(30) NOT NULL,
    `DOB` DATE NOT NULL,
    `phone_number` VARCHAR(14) NOT NULL,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;


-- --------------------
-- USER
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`user` (
	`user_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(20),
    `password` VARCHAR(20),
    `role` VARCHAR(20),
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;


-- --------------------
-- EMPLOYEE
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`employee` (
	`employee_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_ID` INT NOT NULL,
    `personal_information_ID` INT,
    `schedule_ID` INT,
    `wage` FLOAT(8, 2) NOT NULL,
    `title` VARCHAR(20) NOT NULL,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- CUSTOMER
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`customer` (
	`customer_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_ID` INT NOT NULL,
    `personal_information_ID` INT,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- EMERGENCY CONTACT
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`emergency_contact` (
	`personal_information_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(30) NOT NULL,
	`phone_number` VARCHAR(14) NOT NULL,
	`relationship` VARCHAR(20) NOT NULL,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- PRODUCT
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`product` (
	`product_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `store_ID` INT NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `price` FLOAT(3, 2) NOT NULL,
    `quantity` INT NOT NULL,
    `isle_number` INT NOT NULL,
    `minimum_age` INT NOT NULL,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- ORDER
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`order` (
	`order_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `personal_information_ID` INT NOT NULL,
    `total_cost` FLOAT(4, 2) DEFAULT 0,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- ITEM
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`item` (
	`item_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `product_ID` INT NOT NULL,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- SCHEDULE
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`schedule` (
	`schedule_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `time` INT,
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;



-- --------------------
-- ADDRESS
-- --------------------
CREATE TABLE IF NOT EXISTS `grocery_store`.`address` (
	`address_ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `street_address` VARCHAR(20),
    `city` VARCHAR(15),
    `zip` INT(5),
    `deleted` BOOLEAN DEFAULT FALSE
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
