import pandas as pd
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import streamlit as st


def execute_query(query: str, return_df: bool = False, return_column_names: bool = True):
    """
    Builds the database connection and handles the user queries and returns the result as a dataframe.
    """

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)

        if cursor is None or cursor.empty:
            st.warning("Couldn't connect to database - using demo data")
            return 100 

        if return_df:
            result = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            result = result.reset_index(drop=True)
            return result
        
        rows = cursor.fetchall()
        if not return_column_names:
            return rows

        return rows, [desc[0] for desc in cursor.description]
        

    except psycopg2.Error as e:
        print(f"An error occured: {e}")
        return None
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    