import streamlit as st   
from src.assets.styles.styling import styled_write



def about():    
    styled_write("""
                A database was initially used for data ingestion. For deployment, I switched to a static CSV for simplicity. 
                A database version with prediction logging and retraining functionality is in progress.
                """)
   