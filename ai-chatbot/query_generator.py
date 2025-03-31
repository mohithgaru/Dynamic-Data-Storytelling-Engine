from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import re

# Load OpenAI Model
openai_api_key = "your-api-key"
llm = OpenAI(api_key=openai_api_key)

# Define AI Prompt
query_prompt = PromptTemplate(
    input_variables=["question"],
    template="Convert this into an SQL query: {question}"
)

# Function to Validate SQL Queries
def is_valid_sql(query):
    sql_keywords = ["SELECT", "UPDATE", "DELETE", "INSERT", "FROM", "WHERE", "JOIN", "ORDER BY", "GROUP BY"]
    return any(keyword in query.upper() for keyword in sql_keywords) and not re.search(r"DROP|ALTER|DELETE\s+\*", query, re.IGNORECASE)

# Function to Convert User Query to SQL
def generate_sql_query(user_question):
    try:
        query = query_prompt.format(question=user_question)
        sql_query = llm.generate(query)

        # Validate SQL Query
        if not is_valid_sql(sql_query):
            return "⚠️ Invalid SQL Query Generated!"
        
        return sql_query
    except Exception as e:
        return f"❌ AI Query Generation Error: {e}"

# Example Usage
if __name__ == "__main__":
    user_input = "Show total sales for each country."
    sql_query = generate_sql_query(user_input)
    print("Generated SQL Query:", sql_query)
