This enables exploration of SQL queries on a few small tables of joinable seed
data that are loaded to three common engines: SQLite, PostgreSQL, MySQL.

## Prerequisites

- [Docker](https://www.docker.com) for starting fresh/isolated containers for
  PostgreSQL and MySQL

## Why

This project was created to demonstrate some uses of a handful of Python
packages that I maintain:

- [settings-helper](https://pypi.org/project/settings-helper), a wrapper to the
  builtin [configparser
  module](https://docs.python.org/3/library/configparser.html) for loading
  configuration data from a settings.ini file
- [sql-helper](https://pypi.org/project/sql-helper), a wrapper to the
  [SQLAlchemy](https://pypi.org/project/SQLAlchemy) package for interacting with
  SQL databases
- [bg-helper](https://pypi.org/project/bg-helper), a wrapper to the builtin
  [subprocess module](https://docs.python.org/3/library/subprocess.html), that
  includes tools for using docker to manage database containers

## What

There is a `sql_clients.py` file that creates instances of the SQL class from
sql-helper that are connected to the `sqlite_url`, `postgresql_url`, and
`mysql_url` values in the `settings.ini` file (as `sqllite_client`,
`postgresql_client`, and `mysql_client`).

There is a `start-clients.sh` shell script that will start the IPython shell if
it's installed to the venv (falling back to default python), with the
`sql_clients.py` file loaded in interactive mode.

There is a `start-sql.sh` shell script that will start the PostgreSQL and MySQL
containers using the values in the `settings.ini` file and load the seed data if
it has not been loaded before. It also loads the seed data to the SQLite
database.

## Setup

Create a Python virtual environment, then use pip to install the packages listed
in the `requirements.txt` file.

```
venv-setup
```

The [venv-setup](https://github.com/kenjyco/base/blob/master/bin/venv-setup)
script (provided by my [base repo](https://github.com/kenjyco/base)) will create
a virtual environment named venv, use pip to install the dependencies listed in
`requirements.txt`, then use pip to also install the ipython, pytest, and pdbpp
packages. (*You can use `venv-setup-lite` to do all that except for adding the
last 3 packages if desired*).

## Running

Ensure that docker is running and the database instances are started with their
seed data.

```
./start-sql.sh
```

On the first run, you will see docker commands and their output, followed by
messages about data insertions before the script exits.

```
...
Inserted 15 rows into users
Inserted 15 rows into products
Inserted 15 rows into orders
```

On subsequent runs, you will see docker commands and their output, followed by
messages saying data has already been inserted.

```
...
users already has data, skipping insert
products already has data, skipping insert
orders already has data, skipping insert
```

## Usage

Use the `start-clients.sh` shell script to execute the `sql_clients.py` script
in interactive mode.

```
./start-clients.sh
```

The primary objects you will be interacting with during the interactive session
are `sqlite_client`, `postgres_client`, or `mysql_client`. You can pass SQL
queries to the `execute` method on those client objects or use some of the
schema exploration methods (like `get_tables`, `get_columns`,
`get_timestamp_columns`, `get_required_columns`, `get_schemas`, `get_indexes`,
`get_autoincrement_columns`, etc)

```
[ins] In [1]: postgres_client.get_tables()
Out[1]: ['public.orders', 'public.products', 'public.users']

[ins] In [2]: mysql_client.get_tables()
Out[2]: ['orders', 'products', 'users']

[ins] In [3]: sqlite_client.get_tables()
Out[3]: ['orders', 'products', 'users']

[ins] In [4]: postgres_client.get_columns("orders")
Out[4]:
[{'name': 'order_id',
  'type': INTEGER(),
  'nullable': False,
  'default': None,
  'autoincrement': False,
  'comment': None},
 {'name': 'user_id',
  'type': INTEGER(),
  'nullable': True,
  'default': None,
  'autoincrement': False,
  'comment': None},
 {'name': 'product_id',
  'type': INTEGER(),
  'nullable': True,
  'default': None,
  'autoincrement': False,
  'comment': None},
 {'name': 'quantity',
  'type': INTEGER(),
  'nullable': True,
  'default': None,
  'autoincrement': False,
  'comment': None},
 {'name': 'order_date',
  'type': DATE(),
  'nullable': True,
  'default': None,
  'autoincrement': False,
  'comment': None}]

[ins] In [5]: postgres_client.get_columns("orders", name_only=True)
Out[5]: ['order_id', 'user_id', 'product_id', 'quantity', 'order_date']

[ins] In [6]: postgres_client.get_timestamp_columns("orders")
Out[6]:
[{'name': 'order_date',
  'type': DATE(),
  'nullable': True,
  'default': None,
  'autoincrement': False,
  'comment': None}]

[ins] In [7]: postgres_client.execute("SELECT * FROM users LIMIT 5")
Out[7]:
[{'user_id': 1,
  'username': 'alice',
  'email': 'alice@example.com',
  'signup_date': datetime.date(2022, 1, 5),
  'is_active': True},
 {'user_id': 2,
  'username': 'bob',
  'email': 'bob@gmail.com',
  'signup_date': datetime.date(2022, 1, 20),
  'is_active': False},
 {'user_id': 3,
  'username': 'carol',
  'email': 'carol@outlook.com',
  'signup_date': datetime.date(2022, 2, 1),
  'is_active': True},
 {'user_id': 4,
  'username': 'dave',
  'email': 'dave@example.com',
  'signup_date': datetime.date(2022, 2, 15),
  'is_active': True},
 {'user_id': 5,
  'username': 'erin',
  'email': 'erin@aol.com',
  'signup_date': datetime.date(2022, 3, 3),
  'is_active': False}]

[ins] In [8]: postgres_client.execute("SELECT username FROM users LIMIT 5")
Out[8]: ['alice', 'bob', 'carol', 'dave', 'erin']

[ins] In [9]: postgres_client.execute("SELECT username, email FROM users LIMIT 5")
Out[9]:
[{'username': 'alice', 'email': 'alice@example.com'},
 {'username': 'bob', 'email': 'bob@gmail.com'},
 {'username': 'carol', 'email': 'carol@outlook.com'},
 {'username': 'dave', 'email': 'dave@example.com'},
 {'username': 'erin', 'email': 'erin@aol.com'}]

[ins] In [10]: postgres_client.execute("SELECT * FROM products WHERE price > 50.00")
Out[10]:
[{'product_id': 8,
  'name': 'Headphones',
  'category': 'Electronics',
  'price': Decimal('99.99'),
  'stock': 40},
 {'product_id': 9,
  'name': 'Blender',
  'category': 'Kitchen',
  'price': Decimal('55.00'),
  'stock': 25},
 {'product_id': 11,
  'name': 'Running Shoes',
  'category': 'Fitness',
  'price': Decimal('85.00'),
  'stock': 20},
 {'product_id': 13,
  'name': 'Monitor 24”',
  'category': 'Electronics',
  'price': Decimal('149.99'),
  'stock': 10},
 {'product_id': 14,
  'name': 'Standing Desk',
  'category': 'Furniture',
  'price': Decimal('250.00'),
  'stock': 5}]

[ins] In [11]: postgres_client.execute("SELECT email FROM users WHERE email LIKE '%@example.com'")
Out[11]:
['alice@example.com',
 'dave@example.com',
 'frank@example.com',
 'grace@example.com',
 'heidi@example.com',
 'judy@example.com',
 'kim@example.com',
 'leo@example.com',
 'maya@example.com',
 'nick@example.com',
 'olivia@example.com']

[ins] In [12]: postgres_client.execute("SELECT MAX(price) AS highest_price, MIN(price) as lowest_price FROM products")
Out[12]: {'highest_price': Decimal('250.00'), 'lowest_price': Decimal('8.50')}

[ins] In [13]: mysql_client.execute("SELECT MAX(price) AS highest_price, MIN(price) as lowest_price FROM products")
Out[13]: {'highest_price': Decimal('250.00'), 'lowest_price': Decimal('8.50')}

[ins] In [14]: sqlite_client.execute("SELECT MAX(price) AS highest_price, MIN(price) as lowest_price FROM products")
Out[14]: {'highest_price': 250, 'lowest_price': 8.5}

[ins] In [15]: postgres_client.execute("SELECT category, AVG(price) AS avg_price FROM products GROUP BY category ORDER BY avg_price")
Out[15]:
[{'category': 'Stationery', 'avg_price': Decimal('10.0000000000000000')},
 {'category': 'Kitchen', 'avg_price': Decimal('25.1666666666666667')},
 {'category': 'Apparel', 'avg_price': Decimal('27.5000000000000000')},
 {'category': 'Fitness', 'avg_price': Decimal('56.5000000000000000')},
 {'category': 'Electronics', 'avg_price': Decimal('68.0940000000000000')},
 {'category': 'Furniture', 'avg_price': Decimal('142.4750000000000000')}]

[ins] In [16]: mysql_client.execute("SELECT category, AVG(price) AS avg_price FROM products GROUP BY category ORDER BY avg_price")
Out[16]:
[{'category': 'Stationery', 'avg_price': Decimal('10.000000')},
 {'category': 'Kitchen', 'avg_price': Decimal('25.166667')},
 {'category': 'Apparel', 'avg_price': Decimal('27.500000')},
 {'category': 'Fitness', 'avg_price': Decimal('56.500000')},
 {'category': 'Electronics', 'avg_price': Decimal('68.094000')},
 {'category': 'Furniture', 'avg_price': Decimal('142.475000')}]

[ins] In [17]: sqlite_client.execute("SELECT category, AVG(price) AS avg_price FROM products GROUP BY category ORDER BY avg_price")
Out[17]:
[{'category': 'Stationery', 'avg_price': 10.0},
 {'category': 'Kitchen', 'avg_price': 25.166666666666668},
 {'category': 'Apparel', 'avg_price': 27.5},
 {'category': 'Fitness', 'avg_price': 56.5},
 {'category': 'Electronics', 'avg_price': 68.09400000000001},
 {'category': 'Furniture', 'avg_price': 142.475}]

[ins] In [18]: postgres_client.execute("SELECT DISTINCT category FROM products ORDER BY category")
Out[18]: ['Apparel', 'Electronics', 'Fitness', 'Furniture', 'Kitchen', 'Stationery']

[nav] In [19]: mysql_client.execute("SELECT DISTINCT category FROM products ORDER BY category")
Out[19]: ['Apparel', 'Electronics', 'Fitness', 'Furniture', 'Kitchen', 'Stationery']

[ins] In [20]: sqlite_client.execute("SELECT DISTINCT category FROM products ORDER BY category")
Out[20]: ['Apparel', 'Electronics', 'Fitness', 'Furniture', 'Kitchen', 'Stationery']

[ins] In [21]: postgres_client.execute("SELECT user_id, SUM(quantity) AS total_items FROM orders GROUP BY user_id HAVING SUM(quantity) >= 3")
Out[21]:
[{'user_id': 5, 'total_items': 3},
 {'user_id': 10, 'total_items': 4},
 {'user_id': 12, 'total_items': 3},
 {'user_id': 1, 'total_items': 3}]

[ins] In [22]: mysql_client.execute("SELECT user_id, SUM(quantity) AS total_items FROM orders GROUP BY user_id HAVING SUM(quantity) >= 3")
Out[22]:
[{'user_id': 1, 'total_items': Decimal('3')},
 {'user_id': 5, 'total_items': Decimal('3')},
 {'user_id': 10, 'total_items': Decimal('4')},
 {'user_id': 12, 'total_items': Decimal('3')}]

[ins] In [23]: sqlite_client.execute("SELECT user_id, SUM(quantity) AS total_items FROM orders GROUP BY user_id HAVING SUM(quantity) >= 3")
Out[23]:
[{'user_id': 1, 'total_items': 3},
 {'user_id': 5, 'total_items': 3},
 {'user_id': 10, 'total_items': 4},
 {'user_id': 12, 'total_items': 3}]
```
