import streamlit as st
import pandas as pd
import mysql.connector

# MySQL Connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost", user="root", password="yourpassword", database="DynamicInsights"
        )
    except mysql.connector.Error as err:
        st.error(f"❌ Database Connection Error: {err}")
        return None

# Function to detect column types dynamically
def infer_sql_column_types(df):
    type_mapping = {
        'int64': 'INT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN'
    }
    return ", ".join([f"{col} {type_mapping.get(str(df[col].dtype), 'VARCHAR(255)')}" for col in df.columns])

# Streamlit UI
st.title("📊 Dynamic Data Storytelling Engine")
uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📌 Preview of Dataset:")
    st.write(df.head())

    # Convert Column Names to SQL Format
    columns_sql = infer_sql_column_types(df)

    # Create Table in MySQL
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"CALL CreateDynamicTable('{uploaded_file.name.split('.')[0]}', '{columns_sql}')")
            conn.commit()
            st.success("✅ Table Created Successfully in MySQL!")
        except mysql.connector.Error as err:
            st.error(f"⚠️ Error: {err}")
        finally:
            cursor.close()
            conn.close()
