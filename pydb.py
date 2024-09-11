import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sdp',
            user='root',
            password='root123'
        )

        if connection.is_connected():
            print('Successfully connected to the database')
            cursor = connection.cursor()

            # Create table
            create_table_query = """
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INT,
                    gender VARCHAR(10)
                )
            """
            cursor.execute(create_table_query)
            print("Table 'students' created successfully")

            # Insert records
            insert_query = """
                INSERT INTO students (name, age, gender)
                VALUES (%s, %s, %s)
            """
            student_records = [
                ('alice', 22, 'female'),
                ('bob', 24, 'male'),
                ('charlie', 32, 'male')
            ]
            cursor.executemany(insert_query, student_records)
            connection.commit()
            print(f"{cursor.rowcount} records inserted into 'students' table")

            # Select records
            select_query = "SELECT * FROM students"
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Fetching data from 'students' table:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}")

            # Update records
            update_query = """
                UPDATE students
                SET age = %s
                WHERE name = %s
            """
            data_to_update = (25, 'alice')
            cursor.execute(update_query, data_to_update)
            connection.commit()
            print(f"Record updated for {cursor.rowcount} student(s).")

            # Verify the update
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Data after update:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}")

            # Delete records
            delete_query = "DELETE FROM students WHERE name = %s"
            name_to_delete = ('bob',)
            cursor.execute(delete_query, name_to_delete)
            connection.commit()
            print(f"Record deleted for {cursor.rowcount} student(s).")

            # Verify the deletion
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Data after deletion:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}")

            # Drop table
            drop_table_query = "DROP TABLE IF EXISTS students"
            cursor.execute(drop_table_query)
            print("Table 'students' dropped successfully.")

            # Close the cursor
            cursor.close()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Call the function to execute CRUD operations
connect_to_database()
