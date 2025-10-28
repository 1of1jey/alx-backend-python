#!/usr/bin/env python3


import os
from seed import (
    connect_db,
    create_database,
    connect_to_prodev,
    create_table,
    insert_data,
)


def main():
    # 1) connect to MySQL server
    connection = connect_db()
    if not connection:
        print("Could not connect to MySQL server. Check credentials and server status.")
        return

    # 2) create the database if needed
    create_database(connection)
    connection.close()
    print("connection successful")

    # 3) connect to ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        print("Could not connect to ALX_prodev database.")
        return

    # 4) create table and seed data
    create_table(connection)
    csv_path = os.path.join(os.path.dirname(__file__), 'user_data.csv')
    insert_data(connection, csv_path)

    # 5) verify database exists and show first 5 rows
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present ")

        cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()
