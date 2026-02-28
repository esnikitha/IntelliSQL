import sqlite3

# Establish connection to database (creates file if not exists)
connection = sqlite3.connect("data.db")

# Create cursor object
cursor = connection.cursor()

# Create table
create_table_query = """
CREATE TABLE IF NOT EXISTS Students (
    name VARCHAR(30),
    class VARCHAR(10),
    marks INT,
    company VARCHAR(30)
)
"""

cursor.execute(create_table_query)

# Insert records
cursor.execute("INSERT INTO Students VALUES('Sijo', 'BTech', 75, 'JSW')")
cursor.execute("INSERT INTO Students VALUES('Lijo', 'MTech', 69, 'TCS')")
cursor.execute("INSERT INTO Students VALUES('Rijo', 'BSc', 79, 'WIPRO')")
cursor.execute("INSERT INTO Students VALUES('Sibin', 'MSc', 89, 'INFOSYS')")
cursor.execute("INSERT INTO Students VALUES('Dilsha', 'MCom', 99, 'Cyient')")

print("The inserted records are:")

# Query data
cursor.execute("SELECT * FROM Students")

rows = cursor.fetchall()

for row in rows:
    print(row)

# Commit and close
connection.commit()
connection.close()