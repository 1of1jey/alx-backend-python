from typing import Optional
import os
import csv
import uuid
import mysql.connector
from mysql.connector import errorcode


def connect_db() -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """Connect to the MySQL server (no database selected).

    Uses environment variables if present. Returns a connection or None on failure.
    """
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")

    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None


def create_database(connection: mysql.connector.connection_cext.CMySQLConnection) -> None:
    """Create the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        raise
    finally:
        cursor.close()


def connect_to_prodev() -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """Connect to the ALX_prodev database and return the connection."""
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")

    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database="ALX_prodev")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def create_table(connection: mysql.connector.connection_cext.CMySQLConnection) -> None:
    """Create the user_data table if it does not exist."""
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "user_id VARCHAR(36) NOT NULL PRIMARY KEY,"
        "name VARCHAR(255) NOT NULL,"
        "email VARCHAR(255) NOT NULL,"
        "age DECIMAL(5,0) NOT NULL,"
        "UNIQUE KEY email_unique (email)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )

    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        raise
    finally:
        cursor.close()


def insert_data(connection: mysql.connector.connection_cext.CMySQLConnection, data: str) -> None:
    """Insert data from CSV file into user_data table.

    data: path to CSV file, expects header with name,email,age
    Inserts only if the email does not already exist in the table.
    """
    if not os.path.exists(data):
        raise FileNotFoundError(f"CSV file not found: {data}")

    cursor = connection.cursor()
    inserted = 0
    try:
        with open(data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get('name')
                email = row.get('email')
                age = row.get('age')

                if not name or not email or age is None:
                    continue

                # Check existence by email
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s LIMIT 1", (email,))
                if cursor.fetchone():
                    continue

                user_id = str(uuid.uuid4())

                # Use DECIMAL/INT for age; cast to int if possible
                try:
                    age_val = int(age)
                except (ValueError, TypeError):
                    # Fallback to 0 if age malformed
                    age_val = 0

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age_val),
                )
                inserted += 1

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()

    print(f"Inserted {inserted} new rows into user_data")


if __name__ == '__main__':
    # Simple CLI to run the seeding from command line
    conn = connect_db()
    if not conn:
        raise SystemExit(1)

    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    if not conn:
        raise SystemExit(1)

    create_table(conn)
    csv_path = os.path.join(os.path.dirname(__file__), 'user_data.csv')
    try:
        insert_data(conn, csv_path)
    finally:
        conn.close()
