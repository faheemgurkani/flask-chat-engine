import pandas as pd
import sqlite3


def create_connection():

    try:
        connection = sqlite3.connect('final.db')

        return connection

    except sqlite3.Error as e:
        print("Error: Failure in connecting to SQLite", e)

        return None

def create_table(connection):
    try:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                referenceColumnID INTEGER PRIMARY KEY,
                Product_Titles TEXT,
                Prices TEXT,
                Ratings TEXT,
                Ratings_Count TEXT,
                Question_Count TEXT,
                Specifications TEXT,
                Reviews TEXT,
                URLs TEXT
            )
        ''')

        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        print("Error: Table creation failed", e)

def insert_data_to_database(connection, data_frame):

    try:
        cursor = connection.cursor()

        for index, row in data_frame.iterrows():
            cursor.execute('''
                INSERT INTO Products (Product_Titles, Prices, Ratings, Ratings_Count, Question_Count, Specifications, Reviews, URLs) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            row['Product-Titles'], row['Prices'], row['Ratings'], row["Ratings-Count"], row["Question-Count"],
            row['Specifications'], row["Reviews"], row["URLs"]))

        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        print("Error: Database insertion failed", e)

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    daraz_df = pd.read_csv('daraz.csv')

    # Establishing a connection to SQLite
    sqlite_connection = create_connection()

    if sqlite_connection:
        # Creating a table
        create_table(sqlite_connection)

        # Inserting data into the SQLite database
        insert_data_to_database(sqlite_connection, daraz_df)

        print("Data from daraz.csv inserted into the SQLite database.")
