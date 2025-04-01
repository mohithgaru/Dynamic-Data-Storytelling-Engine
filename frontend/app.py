import streamlit as st
import pandas as pd
import mysql.connector
import os

# Ensure MySQL Connector is installed on Streamlit Cloud
os.system("pip install mysql-connector-python")

# Load environment variables (Use secrets in Streamlit Cloud)
DB_HOST = os.getenv("DB_HOST", "your-database-host")
DB_USER = os.getenv("DB_USER", "your-username")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your-password")
DB_NAME = os.getenv("DB_NAME", "DynamicInsights")

# MySQL Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"❌ Database Connection Error: {err}")
        return None

# Function to detect column types dynamically
def infer_sql_column_types(df):
    type_mapping = {
        "int64": "INT",
        "float64": "FLOAT",
        "object": "VARCHAR(255)",
        "bool": "BOOLEAN",
    }
    return ", ".join(
        [f"{col} {type_mapping.get(str(df[col].dtype), 'VARCHAR(255)')}" for col in df.columns]
    )

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
            table_name = uploaded_file.name.split(".")[0]
            
            # Create table dynamically
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_sql});")
            conn.commit()
            
            st.success(f"✅ Table `{table_name}` Created Successfully in MySQL!")
        except mysql.connector.Error as err:
            st.error(f"⚠️ Error: {err}")
        finally:
            cursor.close()
            conn.close()
