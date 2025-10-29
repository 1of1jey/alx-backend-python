#!/usr/bin/env python3
from seed import connect_to_prodev


def stream_user_ages():
    conn = connect_to_prodev()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            # row[0] should be the age (DECIMAL stored); convert to int
            try:
                yield int(row[0])
            except Exception:
                # skip malformed values
                continue
    finally:
        cursor.close()
        conn.close()


def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    average = 0.0
    if count:
        average = total / count

    print(f"Average age of users: {average:.2f}")


if __name__ == '__main__':
    calculate_average_age()
