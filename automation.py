import mysql.connector
import psycopg2

# Connect to MySQL
connection = mysql.connector.connect(user='root', 
                                     password='MTE0NDgtZGViYWJy', 
                                     host='127.0.0.1', 
                                     database='sales')

# Connect to PostgreSQL
dsn_hostname = '127.0.0.1'
dsn_user = 'postgres'
dsn_pwd = 'MjkyMzUtZGViYWJy'
dsn_port = "5432"
dsn_database = "sales"

# Create PostgreSQL connection
conn = psycopg2.connect(
    database=dsn_database,
    user=dsn_user,
    password=dsn_pwd,
    host=dsn_hostname,
    port=dsn_port
)

def get_last_rowid():
    SQL = "SELECT row_id FROM sales_data ORDER BY row_id DESC LIMIT 1;"
    try:
        # Create a cursor object to execute the query
        with conn.cursor() as cursor:
            # Execute the query
            cursor.execute(SQL)

            # Fetch the result
            result = cursor.fetchone()

            # Check if there is a result
            if result:
                # Return the last rowid
                return result[0]
            else:
                return None
    except Exception as e:
        print(f"Error in get_last_rowid: {e}")

last_row_id = get_last_rowid()
print("Last row id on production data warehouse =", last_row_id)

def get_latest_records(lastrowid):
    try:
        # Create a cursor object to execute the query
        with connection.cursor() as cursor:
            # Construct the SQL query to fetch records with rowid greater than lastrowid
            query = f"SELECT * FROM sales_data WHERE rowid > {lastrowid};"

            # Execute the query
            cursor.execute(query)

            # Fetch all the records
            new_records = cursor.fetchall()

            # Return the result
            return new_records
    except Exception as e:
        print(f"Error in get_latest_records: {e}")

new_records = get_latest_records(last_row_id)
print("New rows on staging data warehouse =", len(new_records))

def insert_records(records):
    try:
        # Create a cursor object to execute the query
        with conn.cursor() as cursor:
            # Construct the SQL query for insertion
            query = "INSERT INTO sales_data VALUES (%s, %s, %s , 0, %s)"

            # Iterate over records and insert them
            for record in records:
                cursor.execute(query, record)

        # Commit the changes
        conn.commit()
    except Exception as e:
        print(f"Error in insert_records: {e}")

insert_records(new_records)
print("New rows inserted into production data warehouse =", len(new_records))

# Disconnect from MySQL warehouse
connection.close()

# Disconnect from PostgreSQL data warehouse
conn.close()