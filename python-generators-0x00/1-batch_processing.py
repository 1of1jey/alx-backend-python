#!/usr/bin/env python3
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    if batch_size <= 0:
        return

    conn = connect_to_prodev()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        conn.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                age_val = int(user.get('age', 0))
            except Exception:
                # skip rows with malformed age
                continue

            if age_val > 25:
                print(user)
