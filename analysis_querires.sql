CREATE DATABASE smart_sales_db;
USE smart_sales_db;

DROP TABLE IF EXISTS data;

CREATE TABLE retail_sales (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10,2),
    CustomerID INT,
    Country VARCHAR(100),
    TotalAmount DECIMAL(10,2)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Clean_Online_Retail.csv'
INTO TABLE retail_sales
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select*from retail_sales;


--  the best sellers

SELECT 
    Description, 
    SUM(Quantity) AS Total_Quantity_Sold, 
    ROUND(SUM(TotalAmount), 2) AS Total_Revenue
FROM retail_sales
GROUP BY Description
ORDER BY Total_Revenue DESC
LIMIT 10;


-- who spend the most

SELECT 
    CustomerID, 
    Country,
    COUNT(DISTINCT InvoiceNo) AS Number_of_Orders,
    ROUND(SUM(TotalAmount), 2) AS Total_Spent
FROM retail_sales
GROUP BY CustomerID, Country
ORDER BY Total_Spent DESC
LIMIT 10;



-- monthly sales trend
SELECT 
    YEAR(InvoiceDate) AS Year,
    MONTHNAME(InvoiceDate) AS Month,
    ROUND(SUM(TotalAmount), 2) AS Monthly_Revenue
FROM retail_sales
GROUP BY Year, Month, MONTH(InvoiceDate)
ORDER BY Year, MONTH(InvoiceDate);
