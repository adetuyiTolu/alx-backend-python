import mysql.connector
import csv
import uuid

#configuration for mySQL Database
DB_CONFIG = {
    'user':'root',
    'password':'password',
    'host':'localhost'
}
#
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'

def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print (f"Error:{err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Couldn't create Database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(database=DB_NAME,**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to DB: {err}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            )
        """)
        print(f"Table '{TABLE_NAME}' created.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        with open(data, newline="") as user_data:
            reader = csv.DictReader(user_data)
            for data in reader:
                user_id = str(uuid.uuid4())
                cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE email = %s", (data['email'],))
                if not cursor.fetchone():
                    cursor.execute(f"""
                        INSERT INTO {TABLE_NAME} (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, data['name'],data['email'], data['age']))
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
    return connection,data