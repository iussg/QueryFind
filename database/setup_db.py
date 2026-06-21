import os
import random
from datetime import date, timedelta
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

DB_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce.db')

def create_database():
    if os.path.exists(DB_PATH):
        print("Database already exists. Skipping creation.")
        return

    engine = create_engine(f'sqlite:///{DB_PATH}')

    with engine.connect() as conn:
        # Create tables
        conn.execute(text("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )"""))

        conn.execute(text("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL,
            cost_price REAL,
            stock_quantity INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at DATE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )"""))

        conn.execute(text("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            city TEXT,
            state TEXT,
            country TEXT DEFAULT 'India',
            signup_date DATE,
            is_premium INTEGER DEFAULT 0
        )"""))

        conn.execute(text("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date DATE,
            status TEXT,
            total_amount REAL,
            shipping_city TEXT,
            payment_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )"""))

        conn.execute(text("""
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            discount_percent REAL DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )"""))

        # Seed categories
        categories = [
            ('Electronics', 'Gadgets, phones, laptops and accessories'),
            ('Clothing', 'Men and women fashion and apparel'),
            ('Books', 'Fiction, non-fiction, academic and more'),
            ('Home & Kitchen', 'Appliances, cookware and home decor'),
            ('Sports', 'Fitness equipment and sportswear'),
            ('Beauty', 'Skincare, haircare and cosmetics'),
            ('Toys', 'Kids toys and games'),
            ('Groceries', 'Daily essentials and food items'),
            ('Footwear', 'Shoes, sandals and boots'),
            ('Stationery', 'Office and school supplies'),
        ]
        for cat in categories:
            conn.execute(text("INSERT INTO categories (name, description) VALUES (:n, :d)"),
                         {'n': cat[0], 'd': cat[1]})

        # Seed products
        product_data = [
            ('iPhone 14', 1, 79999, 60000), ('Samsung Galaxy S23', 1, 69999, 52000),
            ('OnePlus Nord 3', 1, 29999, 22000), ('Boat Earbuds', 1, 2499, 1200),
            ('Mi Power Bank', 1, 1299, 700), ('Laptop Stand', 1, 1799, 900),
            ('Men Formal Shirt', 2, 899, 400), ('Women Kurti', 2, 699, 300),
            ('Denim Jeans', 2, 1499, 700), ('Graphic Tee', 2, 499, 200),
            ('Winter Jacket', 2, 2999, 1500), ('Saree', 2, 1999, 900),
            ('Atomic Habits', 3, 399, 150), ('Rich Dad Poor Dad', 3, 299, 120),
            ('Wings of Fire', 3, 249, 100), ('Python Programming', 3, 599, 250),
            ('The Alchemist', 3, 199, 80), ('Zero to One', 3, 449, 180),
            ('Pressure Cooker', 4, 1299, 600), ('Non-stick Pan', 4, 799, 350),
            ('Air Fryer', 4, 4999, 2500), ('Water Purifier', 4, 8999, 4500),
            ('Mixer Grinder', 4, 3499, 1800), ('Dinner Set', 4, 1999, 900),
            ('Yoga Mat', 5, 699, 300), ('Dumbbells 5kg', 5, 999, 500),
            ('Resistance Bands', 5, 399, 180), ('Cricket Bat', 5, 1799, 900),
            ('Badminton Racket', 5, 1299, 600), ('Cycling Gloves', 5, 499, 200),
            ('Face Serum', 6, 899, 350), ('Sunscreen SPF50', 6, 599, 250),
            ('Shampoo 500ml', 6, 349, 140), ('Lipstick Set', 6, 799, 300),
            ('Night Cream', 6, 1099, 450), ('Perfume', 6, 1499, 600),
            ('LEGO Set', 7, 2499, 1200), ('Board Game', 7, 999, 450),
            ('Remote Car', 7, 1299, 600), ('Doll House', 7, 1799, 800),
            ('Basmati Rice 5kg', 8, 499, 280), ('Organic Dal 1kg', 8, 189, 100),
            ('Olive Oil 1L', 8, 699, 400), ('Green Tea 100bags', 8, 299, 140),
            ('Running Shoes', 9, 2999, 1400), ('Formal Shoes', 9, 3499, 1700),
            ('Sports Sandals', 9, 999, 450), ('Canvas Sneakers', 9, 1499, 700),
            ('Notebook Pack', 10, 199, 80), ('Pen Set', 10, 149, 60),
            ('Sticky Notes', 10, 99, 40), ('Stapler', 10, 249, 100),
        ]

        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad',
                  'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
        states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana',
                  'Maharashtra', 'West Bengal', 'Gujarat', 'Rajasthan', 'Uttar Pradesh']

        for p in product_data:
            stock = random.randint(0, 200)
            created = date(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            conn.execute(text("""INSERT INTO products 
                (name, category_id, price, cost_price, stock_quantity, is_active, created_at)
                VALUES (:n, :c, :p, :cp, :s, :a, :cr)"""),
                {'n': p[0], 'c': p[1], 'p': p[2], 'cp': p[3],
                 's': stock, 'a': 1, 'cr': created})

        # Seed customers
        for i in range(500):
            city_idx = random.randint(0, 9)
            signup = date(2022, 1, 1) + timedelta(days=random.randint(0, 900))
            conn.execute(text("""INSERT INTO customers 
                (name, email, city, state, country, signup_date, is_premium)
                VALUES (:n, :e, :c, :s, :co, :sd, :ip)"""),
                {'n': fake.name(), 'e': fake.unique.email(),
                 'c': cities[city_idx], 's': states[city_idx],
                 'co': 'India', 'sd': signup, 'ip': random.choice([0, 0, 0, 1])})

        # Seed orders and order_items
        statuses = ['delivered', 'delivered', 'delivered', 'pending', 'cancelled', 'returned']
        payments = ['UPI', 'UPI', 'Credit Card', 'COD', 'Net Banking']
        order_count = 0
        item_count = 0

        for order_id in range(1, 1001):
            customer_id = random.randint(1, 500)
            city_idx = random.randint(0, 9)
            order_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 900))
            status = random.choice(statuses)
            payment = random.choice(payments)

            # Generate 2-3 items per order
            num_items = random.randint(2, 3)
            total = 0
            items = []
            product_ids = random.sample(range(1, 53), num_items)

            for pid in product_ids:
                qty = random.randint(1, 3)
                # Get product price
                result = conn.execute(text("SELECT price FROM products WHERE product_id=:p"), {'p': pid})
                price = result.fetchone()[0]
                discount = random.choice([0, 0, 5, 10, 15])
                item_total = qty * price * (1 - discount / 100)
                total += item_total
                items.append((pid, qty, price, discount))

            conn.execute(text("""INSERT INTO orders 
                (customer_id, order_date, status, total_amount, shipping_city, payment_method)
                VALUES (:c, :od, :s, :t, :sc, :pm)"""),
                {'c': customer_id, 'od': order_date, 's': status,
                 't': round(total, 2), 'sc': cities[city_idx], 'pm': payment})

            for item in items:
                conn.execute(text("""INSERT INTO order_items 
                    (order_id, product_id, quantity, unit_price, discount_percent)
                    VALUES (:o, :p, :q, :u, :d)"""),
                    {'o': order_id, 'p': item[0], 'q': item[1],
                     'u': item[2], 'd': item[3]})
                item_count += 1
            order_count += 1

        conn.commit()
        print(f"Database created successfully!")
        print(f"  Customers : 500")
        print(f"  Orders    : {order_count}")
        print(f"  Items     : {item_count}")
        print(f"  Products  : {len(product_data)}")
        print(f"  Categories: {len(categories)}")

if __name__ == '__main__':
    create_database()