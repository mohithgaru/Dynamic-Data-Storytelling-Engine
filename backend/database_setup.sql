-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS DynamicInsights;
USE DynamicInsights;

-- Step 2: Track Uploaded Datasets
CREATE TABLE IF NOT EXISTS uploaded_datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Stored Procedure to Check If Table Exists
DELIMITER $$

CREATE PROCEDURE CheckTableExists(IN tableName VARCHAR(255), OUT tableExists BOOLEAN)
BEGIN
    SET @query = CONCAT("SELECT COUNT(*) INTO @count FROM information_schema.tables WHERE table_schema = 'DynamicInsights' AND table_name = '", tableName, "'");
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    SET tableExists = @count > 0;
END $$

DELIMITER ;

-- Step 4: Stored Procedure to Create Dynamic Tables with Correct Data Types
DELIMITER $$

CREATE PROCEDURE CreateDynamicTable(IN tableName VARCHAR(255), IN columnsText TEXT)
BEGIN
    DECLARE tableExists BOOLEAN DEFAULT FALSE;
    
    CALL CheckTableExists(tableName, tableExists);
    
    IF tableExists THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table already exists!';
    ELSE
        SET @sql = CONCAT('CREATE TABLE ', tableName, ' (id INT AUTO_INCREMENT PRIMARY KEY, ', columnsText, ')');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END $$

DELIMITER ;

-- Step 5: Stored Procedure to Generate Insights
DELIMITER $$

CREATE PROCEDURE GetDatasetInsights(IN tableName VARCHAR(255))
BEGIN
    SET @query = CONCAT(
        'SELECT 
            COUNT(*) AS TotalRecords,
            COUNT(DISTINCT CustomerID) AS UniqueCustomers,
            SUM(UnitPrice * Quantity) AS TotalRevenue
        FROM ', tableName);
    
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END $$

DELIMITER ;
