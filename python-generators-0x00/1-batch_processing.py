import sys
import seed
import mysql.connector

def stream_users_in_batches(batch_size):
    connection =seed.connect_to_prodev()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM user_data")
        total_rows = cursor.fetchone()['COUNT(*)']

        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error streaming users in batches: {err}")
    
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        users_over_25 = [user for user in batch if float(user['age']) > 25]
        for user in users_over_25:
            print(f"Name: {user['name']}, Age: {user['age']}, Email: {user['email']}")
 