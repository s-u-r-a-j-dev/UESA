import random
import pandas as pd
import sqlite3

# Define the SQLite database filename
db_filename = 'maindatabase.db'

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Read the Excel file into a Pandas DataFrame
excel_file = 'ktu.xlsx'
df = pd.read_excel(excel_file)

# Specify the table name in the database
table_name = 'Complete_data'
existing_column1 = 'Student'
existing_column2 = 'Roll_no'
existing_column3 = 'YRBR'
# Create the table in the database
df.to_sql(table_name, conn, if_exists='replace', index=False)
cursor.execute(f"CREATE TABLE {table_name}_temp AS SELECT Student, Branch_Name, Session, Exam_Definition FROM {table_name}")

print(f"Data from '{excel_file}' has been saved to '{db_filename}' in table '{table_name}'.")
cursor.execute(f"DROP TABLE {table_name}")
cursor.execute(f"ALTER TABLE {table_name}_temp RENAME TO {table_name}")
cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN Name TEXT")

# 2. Update the new column using an UPDATE statement
cursor.execute(f"UPDATE {table_name} SET Name = SUBSTR({existing_column1}, 1, LENGTH({existing_column1}) - 12)")
cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN Roll_no TEXT")

# 2. Update the new column using an UPDATE statement
cursor.execute(f"UPDATE {table_name} SET Roll_no = SUBSTR({existing_column1}, INSTR({existing_column1}, '(') + 1, INSTR({existing_column1}, ')') - INSTR({existing_column1}, '(') - 1)")
print("New column Roll_no has been added")
cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN YRBR TEXT")

# 2. Update the new column using an UPDATE statement
cursor.execute(f"UPDATE {table_name} SET YRBR = SUBSTR({existing_column2}, LENGTH({existing_column2}) - 6, 4)")
print("New column YRBR has been added")
print("Starting sorting of the complete data")
print("Table has been sorted according to the requirements and moved to a New Table Fulllist_Sorted ")
table2 = 'Fulllist_Sorted'
cursor.execute(f"CREATE TABLE {table2} AS SELECT * FROM {table_name} ORDER BY Branch_Name ASC, {existing_column3} ASC, Roll_no ASC")

# create a new table to separate different departments
print("Separating All Deparments")
table3 = 'CE'
cursor.execute(f"CREATE TABLE {table3} AS SELECT * FROM {table2} WHERE Branch_Name = 'CIVIL ENGINEERING'")

table4 = 'CS'
cursor.execute(f"CREATE TABLE {table4} AS SELECT * FROM {table2} WHERE Branch_Name = 'COMPUTER SCIENCE & ENGINEERING'")

table5 = 'EE'
cursor.execute(f"CREATE TABLE {table5} AS SELECT * FROM {table2} WHERE Branch_Name = 'ELECTRICAL AND ELECTRONICS ENGINEERING'")

table6 = 'EC'
cursor.execute(f"CREATE TABLE {table6} AS SELECT * FROM {table2} WHERE Branch_Name = 'ELECTRONICS & COMMUNICATION ENGG'")

table7 = 'ME'
cursor.execute(f"CREATE TABLE {table7} AS SELECT * FROM {table2} WHERE Branch_Name = 'MECHANICAL ENGINEERING'")
print("Separate Tables have been created for each departments")

num_halls = int(input("Enter the number of halls: "))
table8 = 'Halls_info'
cursor.execute("CREATE TABLE IF NOT EXISTS Halls_info (Hall_number INTEGER PRIMARY KEY,Hall_name TEXT,Capacity INTEGER)")
# Prompt the user to enter hall information
for i in range(1, num_halls + 1):
    hall_number = i
    hall_name = input(f"Enter the name of Hall {i}: ")
    capacity = int(input(f"Enter the capacity of Hall {i}: "))

    # Step 4: Insert the information into the database
    cursor.execute("INSERT INTO Halls_info (Hall_number, Hall_name, Capacity)VALUES (?, ?, ?)", (hall_number, hall_name, capacity))



cursor.execute("SELECT DISTINCT Hall_name FROM Halls_info")
hall_names = [row[0] for row in cursor.fetchall()]

# Create a table for each hall name
for hall_name in hall_names:
    table9 = hall_name.replace(' ', '_')  # Use hall name as the table name
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table9} (Roll_no INTEGER ,Student_name TEXT,Branch TEXT)")

print(f"Tables have been created for each hall name.")

# Commit the changes and close the database connection
conn.commit()
conn.close()

print(f"Data from '{excel_file}' has been saved to '{db_filename}' in table '{table_name}'.")



