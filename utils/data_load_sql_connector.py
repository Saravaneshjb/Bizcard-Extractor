import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector import FieldType
import pandas as pd
import logging



class Dataload:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'bizcard'
        }

    def create_connection(self):
        """ Create a connection to MySQL database """
        try:
            conn = mysql.connector.connect(**self.db_config)
            if conn.is_connected():
                print('Connected to MySQL database')
                logging.info('Connected to MySQL database')
                return conn
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            logging.error(f"Error connecting to MySQL database: {e}")
            return None

    def close_connection(self, conn):
        """ Close connection to MySQL database """
        if conn.is_connected():
            conn.close()
            print('Connection to MySQL database closed')
            logging.info('Connection to MySQL database closed')

    def execute_query(self, query):
        """ Execute SQL query """
        try:
            conn = self.create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query)
                if cursor.description is not None:  # Check if there are any results
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    df = pd.DataFrame(rows, columns=columns)
                    return df
                else:
                    return None  # Return None if no results
        except Error as e:
            print(f"Error executing query: {e}")
            logging.error(f"Error executing query: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def load_df(self, df_data,df_name):
        try:
            conn = self.create_connection()
            if conn:
                # Convert DataFrame to list of tuples
                data = [tuple(row) for row in df_data.values]
                # print(data)
                # Define the INSERT INTO query
                query = f"INSERT INTO {df_name} ({', '.join(df_data.columns)}) VALUES ({', '.join(['%s'] * len(df_data.columns))})"
                print('The insert query being executed is : ',query)
                logging.info(f'The insert query being executed is : {query}')
                # Execute the query
                cursor = conn.cursor()
                cursor.executemany(query, data)
                conn.commit()
                print("Data loaded successfully")
                logging.info("Data loaded successfully")
        finally:
            self.close_connection(conn)
    
    def execute_update_query(self, query):
        """ Execute update query """
        try:
            conn = self.create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print("Update query executed successfully")
                logging.info("Update query executed successfully")
        finally:
            self.close_connection(conn)