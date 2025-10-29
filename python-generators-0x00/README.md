# Python Generators - Database Seeding

## Overview
This project demonstrates database setup and population using Python with MySQL, preparing for generator-based data streaming exercises.

---

## Project Structure

```
python-generators-0x00/
├── seed.py              # Database setup and seeding script
├── user_data.csv        # Sample user data
├── main.py           # Test script
└── README.md           # This file
```

---

## Requirements

### Software
- Python 3.x
- MySQL Server 5.7+
- MySQL Connector for Python

### Installation

```bash
# Install MySQL Connector
pip install mysql-connector-python

# Or using pip3
pip3 install mysql-connector-python
```

---

## Database Schema

### Database: `ALX_prodev`

### Table: `user_data`

| Column | Type | Constraints |
|--------|------|-------------|
| user_id | CHAR(36) | PRIMARY KEY, Indexed |
| name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| age | DECIMAL | NOT NULL |

---

## Functions

### `connect_db()`
Connects to the MySQL database server.

**Returns**: MySQL connection object or None

---

### `create_database(connection)`
Creates the database `ALX_prodev` if it does not exist.

**Args**: connection - MySQL connection object

---

### `connect_to_prodev()`
Connects to the `ALX_prodev` database.

**Returns**: MySQL connection object to ALX_prodev database

---

### `create_table(connection)`
Creates table `user_data` if it does not exist with required fields.

**Args**: connection - MySQL connection object

---

### `insert_data(connection, csv_file)`
Inserts data from CSV into the database if it does not exist.

**Args**:
- connection - MySQL connection object
- csv_file - Path to CSV file

**Features**:
- Skips insertion if data already exists
- Generates UUID for each user
- Batch commit for efficiency
- Error handling and rollback

---

## Usage

### Configuration

Edit `seed.py` to update MySQL credentials:

```python
# In connect_db() and connect_to_prodev()
user='root',        # Your MySQL username
password='',        # Your MySQL password
```

### Running the Script

```bash
# Make executable
chmod +x 0-main.py seed.py

# Run
./0-main.py
```

### Expected Output

```
connection successful
Table user_data created successfully
Successfully inserted 1000 records into user_data table
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

---

## CSV File Format

The `user_data.csv` file should have the following structure:

```csv
"name","email","age"
"John Doe","john@example.com","30"
"Jane Smith","jane@example.com","25"
```

**Note**: 
- Headers are required
- UUID is auto-generated (not in CSV)
- Age should be numeric

---

## Features

### Data Validation
- Checks if database exists before creation
- Checks if table exists before creation
- Checks if data exists before insertion
- Prevents duplicate data insertion

### Error Handling
- Database connection errors
- File not found errors
- SQL execution errors
- Automatic rollback on errors

### UUID Generation
- Each user gets a unique UUID (v4)
- Format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`

---

## Testing

### Verify Database

```sql
-- Connect to MySQL
mysql -u root -p

-- Check database
SHOW DATABASES LIKE 'ALX_prodev';

-- Use database
USE ALX_prodev;

-- Check table
SHOW TABLES;

-- View data
SELECT * FROM user_data LIMIT 5;

-- Count records
SELECT COUNT(*) FROM user_data;
```

### Python Test

```python
#!/usr/bin/python3
import seed

# Test connection
conn = seed.connect_db()
if conn:
    print("✓ Connected to MySQL")
    conn.close()

# Test database creation
conn = seed.connect_db()
seed.create_database(conn)
conn.close()
print("✓ Database created")

# Test table creation
conn = seed.connect_to_prodev()
if conn:
    seed.create_table(conn)
    print("✓ Table created")
    conn.close()
```

---

## Troubleshooting

### Connection Refused
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql
```

### Access Denied
```python
# Update credentials in seed.py
user='your_username',
password='your_password'
```

### Module Not Found
```bash
# Install mysql-connector
pip3 install mysql-connector-python
```

### CSV File Not Found
```bash
# Ensure user_data.csv is in the same directory
ls user_data.csv
```

---

## Next Steps

This project prepares the database for:
- Generator-based data streaming
- Memory-efficient data processing
- Lazy evaluation techniques
- Batch processing implementation

---

## Repository

- **GitHub**: `alx-backend-python`
- **Directory**: `python-generators-0x00`
- **Files**: `seed.py`, `README.md`

