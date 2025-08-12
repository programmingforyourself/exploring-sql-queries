import bg_helper as bh
import settings_helper as sh
import sql_helper as sqh


settings = sh.get_all_settings().get('default')

statement_create_users = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE,
    is_active BOOLEAN
)
"""

statement_create_products = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INTEGER
)
"""

statement_create_orders = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    order_date DATE
)
"""

data_users = [
    {'user_id': 1, 'username': 'alice', 'email': 'alice@example.com', 'signup_date': '2022-01-05', 'is_active': True},
    {'user_id': 2, 'username': 'bob', 'email': 'bob@gmail.com', 'signup_date': '2022-01-20', 'is_active': False},
    {'user_id': 3, 'username': 'carol', 'email': 'carol@outlook.com', 'signup_date': '2022-02-01', 'is_active': True},
    {'user_id': 4, 'username': 'dave', 'email': 'dave@example.com', 'signup_date': '2022-02-15', 'is_active': True},
    {'user_id': 5, 'username': 'erin', 'email': 'erin@aol.com', 'signup_date': '2022-03-03', 'is_active': False},
    {'user_id': 6, 'username': 'frank', 'email': 'frank@example.com', 'signup_date': '2022-03-20', 'is_active': True},
    {'user_id': 7, 'username': 'grace', 'email': 'grace@example.com', 'signup_date': '2022-04-01', 'is_active': True},
    {'user_id': 8, 'username': 'heidi', 'email': 'heidi@example.com', 'signup_date': '2022-04-17', 'is_active': True},
    {'user_id': 9, 'username': 'ivan', 'email': 'ivan@protonmail.com', 'signup_date': '2022-05-01', 'is_active': False},
    {'user_id': 10, 'username': 'judy', 'email': 'judy@example.com', 'signup_date': '2022-05-22', 'is_active': True},
    {'user_id': 11, 'username': 'kim', 'email': 'kim@example.com', 'signup_date': '2022-06-03', 'is_active': False},
    {'user_id': 12, 'username': 'leo', 'email': 'leo@example.com', 'signup_date': '2022-06-14', 'is_active': True},
    {'user_id': 13, 'username': 'maya', 'email': 'maya@example.com', 'signup_date': '2022-07-01', 'is_active': True},
    {'user_id': 14, 'username': 'nick', 'email': 'nick@example.com', 'signup_date': '2022-07-15', 'is_active': True},
    {'user_id': 15, 'username': 'olivia', 'email': 'olivia@example.com', 'signup_date': '2022-08-01', 'is_active': True},
]

data_products = [
    {'product_id': 1, 'name': 'Wireless Mouse', 'category': 'Electronics', 'price': 19.99, 'stock': 100},
    {'product_id': 2, 'name': 'USB-C Charger', 'category': 'Electronics', 'price': 25.50, 'stock': 50},
    {'product_id': 3, 'name': 'Water Bottle', 'category': 'Kitchen', 'price': 12.00, 'stock': 200},
    {'product_id': 4, 'name': 'Desk Lamp', 'category': 'Furniture', 'price': 34.95, 'stock': 75},
    {'product_id': 5, 'name': 'Yoga Mat', 'category': 'Fitness', 'price': 28.00, 'stock': 60},
    {'product_id': 6, 'name': 'Laptop Stand', 'category': 'Electronics', 'price': 45.00, 'stock': 30},
    {'product_id': 7, 'name': 'Notebook Set', 'category': 'Stationery', 'price': 10.00, 'stock': 300},
    {'product_id': 8, 'name': 'Headphones', 'category': 'Electronics', 'price': 99.99, 'stock': 40},
    {'product_id': 9, 'name': 'Blender', 'category': 'Kitchen', 'price': 55.00, 'stock': 25},
    {'product_id': 10, 'name': 'T-Shirt', 'category': 'Apparel', 'price': 15.00, 'stock': 150},
    {'product_id': 11, 'name': 'Running Shoes', 'category': 'Fitness', 'price': 85.00, 'stock': 20},
    {'product_id': 12, 'name': 'Coffee Mug', 'category': 'Kitchen', 'price': 8.50, 'stock': 180},
    {'product_id': 13, 'name': 'Monitor 24”', 'category': 'Electronics', 'price': 149.99, 'stock': 10},
    {'product_id': 14, 'name': 'Standing Desk', 'category': 'Furniture', 'price': 250.00, 'stock': 5},
    {'product_id': 15, 'name': 'Backpack', 'category': 'Apparel', 'price': 40.00, 'stock': 80},
]

data_orders = [
    {'order_id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2, 'order_date': '2022-03-10'},
    {'order_id': 2, 'user_id': 1, 'product_id': 3, 'quantity': 1, 'order_date': '2022-03-11'},
    {'order_id': 3, 'user_id': 2, 'product_id': 2, 'quantity': 1, 'order_date': '2022-03-11'},
    {'order_id': 4, 'user_id': 3, 'product_id': 5, 'quantity': 2, 'order_date': '2022-03-12'},
    {'order_id': 5, 'user_id': 4, 'product_id': 4, 'quantity': 1, 'order_date': '2022-03-13'},
    {'order_id': 6, 'user_id': 5, 'product_id': 7, 'quantity': 3, 'order_date': '2022-03-14'},
    {'order_id': 7, 'user_id': 6, 'product_id': 8, 'quantity': 1, 'order_date': '2022-03-15'},
    {'order_id': 8, 'user_id': 7, 'product_id': 9, 'quantity': 1, 'order_date': '2022-03-15'},
    {'order_id': 9, 'user_id': 8, 'product_id': 1, 'quantity': 1, 'order_date': '2022-03-16'},
    {'order_id': 10, 'user_id': 9, 'product_id': 6, 'quantity': 1, 'order_date': '2022-03-17'},
    {'order_id': 11, 'user_id': 10, 'product_id': 3, 'quantity': 4, 'order_date': '2022-03-18'},
    {'order_id': 12, 'user_id': 11, 'product_id': 10, 'quantity': 2, 'order_date': '2022-03-19'},
    {'order_id': 13, 'user_id': 12, 'product_id': 12, 'quantity': 3, 'order_date': '2022-03-20'},
    {'order_id': 14, 'user_id': 13, 'product_id': 13, 'quantity': 1, 'order_date': '2022-03-21'},
    {'order_id': 15, 'user_id': 14, 'product_id': 15, 'quantity': 1, 'order_date': '2022-03-22'},
]


def insert_if_empty(sql_instance, table_name, data):
    count = sql_instance.execute("SELECT COUNT(*) FROM {}".format(table_name))
    if count == 0:
        sql_instance.insert(table_name, data)
        print("Inserted {} rows into {}".format(len(data), table_name))
    else:
        print("{} already has data, skipping insert".format(table_name))


def load_data(sql_instance):
    sql_instance.execute(statement_create_users)
    sql_instance.execute(statement_create_products)
    sql_instance.execute(statement_create_orders)
    insert_if_empty(sql_instance, 'users', data_users)
    insert_if_empty(sql_instance, 'products', data_products)
    insert_if_empty(sql_instance, 'orders', data_orders)


def start_postgres_docker():
    """Start postgresql container for storing data and insert seed data if missing"""
    bh.tools.docker_ok(exception=True)
    bh.tools.docker_postgres_start(
        settings['postgresql_container_name'],
        version=settings['postgresql_image_version'],
        port=settings['postgresql_port'],
        username=settings['postgresql_username'],
        password=settings['postgresql_password'],
        db=settings['postgresql_db'],
        rm=settings['postgresql_rm'],
        data_dir=settings['postgresql_data_dir'],
        exception=True,
        show=True,
        force=False,
        wait=True,
        sleeptime=2
    )
    sql = sqh.SQL(settings['postgresql_url'])
    load_data(sql)


def start_mysql_docker():
    """Start mysql container for storing data and insert seed data if missing"""
    bh.tools.docker_ok(exception=True)
    bh.tools.docker_mysql_start(
        settings['mysql_container_name'],
        version=settings['mysql_image_version'],
        port=settings['mysql_port'],
        root_password=settings['mysql_root_password'],
        username=settings['mysql_username'],
        password=settings['mysql_password'],
        db=settings['mysql_db'],
        rm=settings['mysql_rm'],
        data_dir=settings['mysql_data_dir'],
        exception=True,
        show=True,
        force=False,
        wait=True,
        sleeptime=2
    )
    sql = sqh.SQL(settings['mysql_url'])
    load_data(sql)


def start_sqlite():
    """Start mysql container for storing data and insert seed data if missing"""
    sql = sqh.SQL(settings['sqlite_url'])
    load_data(sql)


if __name__ == '__main__':
    start_postgres_docker()
    start_mysql_docker()
    start_sqlite()
