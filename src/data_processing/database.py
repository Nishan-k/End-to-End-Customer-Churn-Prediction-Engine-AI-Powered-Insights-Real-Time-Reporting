import pandas as pd
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import streamlit as st


def execute_query(
    query: str, 
    return_df: bool = False, 
    return_column_names: bool = True
):
    """Handles database queries with proper error recovery"""
    conn = None
    try:
        conn = psycopg2.connect(
            **DB_CONFIG,
            connect_timeout=5  
        )
        
        
        with conn.cursor() as cursor:
            cursor.execute(query)
            
            
            if cursor.rowcount == 0:
                st.warning("Query returned no results")
                return pd.DataFrame() if return_df else None
            
          
            if return_df:
                return pd.DataFrame(
                    cursor.fetchall(),
                    columns=[desc[0] for desc in cursor.description]
                )
                
            rows = cursor.fetchall()
            return (rows, [desc[0] for desc in cursor.description]) if return_column_names else rows

    except psycopg2.OperationalError as e:
        st.error(f"🚨 Database connection failed: {e}")
        return pd.DataFrame() if return_df else None  
        
    except Exception as e:
        st.error(f"⚠️ Query failed: {e}")
        return None
        
    finally:
        if conn:
            conn.close()
    