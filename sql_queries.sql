-- Active: 1748390994320@@127.0.0.1@5432@general
SELECT c.name AS client_name, SUM(oi.price * oi.quantity) AS total_amount
FROM
    clients c
    JOIN orders o ON c.id = o.client_id
    JOIN order_items oi ON o.id = oi.order_id
GROUP BY
    c.id,
    c.name
ORDER BY total_amount DESC;

SELECT
    parent.name AS parent_category,
    COUNT(child.id) AS children_count
FROM
    categories parent
    LEFT JOIN categories child ON parent.id = child.parent_id
WHERE
    parent.parent_id IS NULL
GROUP BY
    parent.id,
    parent.name
ORDER BY parent.name;

WITH RECURSIVE
    category_hierarchy AS (
        SELECT
            id,
            name,
            parent_id,
            name as root_category_name,
            0 as level
        FROM categories
        WHERE
            parent_id IS NULL
        UNION ALL
        SELECT c.id, c.name, c.parent_id, ch.root_category_name, ch.level + 1
        FROM
            categories c
            JOIN category_hierarchy ch ON c.parent_id = ch.id
    ),
    product_sales AS (
        SELECT
            p.id as product_id,
            p.name as product_name,
            ch.root_category_name as category_level_1,
            SUM(oi.quantity) as total_quantity
        FROM
            products p
            JOIN category_hierarchy ch ON p.category_id = ch.id
            JOIN order_items oi ON p.id = oi.product_id
            JOIN orders o ON oi.order_id = o.id
        WHERE
            o.created_at >= CURRENT_DATE - INTERVAL '1 month'
        GROUP BY
            p.id,
            p.name,
            ch.root_category_name
    )
SELECT
    product_name as "Наименование товара",
    category_level_1 as "Категория 1-го уровня",
    total_quantity as "Общее количество проданных штук"
FROM product_sales
ORDER BY total_quantity DESC
LIMIT 5;

-- 1) ИНДЕКСЫ для оптимизации

CREATE INDEX idx_orders_created_at ON orders (created_at);

CREATE INDEX idx_order_items_order_product ON order_items (order_id, product_id);

CREATE INDEX idx_products_category_id ON products (category_id);

CREATE INDEX idx_categories_parent_id ON categories (parent_id);

CREATE INDEX idx_orders_client_id ON orders (client_id);

CREATE INDEX idx_order_items_covering ON order_items (order_id, product_id) INCLUDE (quantity, price);

CREATE INDEX idx_orders_date_client ON orders (created_at DESC, client_id);

CREATE INDEX idx_products_category_name ON products (category_id) INCLUDE (name, price);

CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT
    p.name as "Наименование товара",
    parent_cat.name as "Категория 1-го уровня",
    SUM(oi.quantity) as "Общее количество проданных штук"
FROM
    products p
    JOIN categories cat ON p.category_id = cat.id
    JOIN categories parent_cat ON cat.parent_id = parent_cat.id
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
WHERE
    o.created_at >= CURRENT_DATE - INTERVAL '1 month'
    AND parent_cat.parent_id IS NULL
GROUP BY
    p.id,
    p.name,
    parent_cat.name
ORDER BY SUM(oi.quantity) DESC
LIMIT 5;

SELECT * FROM top_5_products_last_month;

-- 2) ПАРТИЦИОНИРОВАНИЕ ДЛЯ БОЛЬШИХ ОБЪЕМОВ
-- Идея: Разделить таблицу orders по месяцам для ускорения запросов

-- CREATE TABLE orders_partitioned (LIKE orders INCLUDING ALL)
-- PARTITION BY
--     RANGE (created_at);

-- CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned FOR
-- VALUES
-- FROM ('2024-01-01') TO ('2024-04-01');

-- CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned FOR
-- VALUES
-- FROM ('2024-04-01') TO ('2024-07-01');

-- CREATE TABLE orders_2024_q3 PARTITION OF orders_partitioned FOR
-- VALUES
-- FROM ('2024-07-01') TO ('2024-10-01');

-- CREATE TABLE orders_2024_q4 PARTITION OF orders_partitioned FOR
-- VALUES
-- FROM ('2024-10-01') TO ('2025-01-01');
