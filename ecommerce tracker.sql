create database ecommerce_tracker;

use ecommerce_tracker;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    link varchar(1000),
    name varchar(300),
    stars DECIMAL(2,1),
    number_of_rating INT,
    number_of_reviews INT,
    disc_price decimal(12,2),
    orig_price decimal(12,2),
    discount varchar(10),
    features varchar(1000),
    scrape_date date
);

SELECT * FROM products;

# Find today’s top discounts:

SELECT name, discount, orig_price, disc_price
FROM products
WHERE scrape_date = CURDATE()
ORDER BY CAST(REPLACE(discount, '% ', '') AS UNSIGNED) DESC
LIMIT 10;

## Track price change overtime

SELECT name, MIN(disc_price) AS lowest_price, MAX(disc_price) AS highest_price
FROM products
GROUP BY name;

## Find products with dropping prices (yesterday vs today):

SELECT p1.name, p1.disc_price AS yesterday_price, p2.disc_price AS today_price
FROM products p1
JOIN products p2
  ON p1.name = p2.name
WHERE p1.scrape_date = CURDATE() - INTERVAL 1 DAY
  AND p2.scrape_date = CURDATE()
  AND p2.disc_price < p1.disc_price;


