from itertools import islice
import seed

def stream_users():
    connection = seed.connect_to_prodev()
    cursor= connection.cursor()
    cursor.execute(f"SELECT * FROM {seed.TABLE_NAME}")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()