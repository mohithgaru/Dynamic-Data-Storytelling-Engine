# 📊 Dynamic Data Storytelling Engine
A SQL-powered insights engine that dynamically generates insights from uploaded datasets.

## 🚀 Features
✅ Upload CSV datasets  
✅ Automatically create MySQL tables (detects correct data types)  
✅ Generate insights (total records, unique values, revenue)  
✅ AI-powered SQL query generation  
✅ Improved error handling & query validation  

## 📂 Project Structure
- **backend/** → MySQL scripts (database & stored procedures)
- **frontend/** → Streamlit app (UI & dataset upload)
- **ai-chatbot/** → AI chatbot for SQL queries  

## 🔧 Setup Instructions
1. Install MySQL & create a database using `database_setup.sql`
2. Install dependencies:  
   ```bash
   pip install streamlit pandas mysql-connector-python langchain openai
