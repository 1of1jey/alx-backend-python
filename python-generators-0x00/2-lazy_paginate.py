#!/usr/bin/env python3
import seed


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


def lazy_pagination(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size


# compatibility: allow either name
lazy_paginate = lazy_pagination
