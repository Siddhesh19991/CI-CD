from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import mysql.connector


# load_dotenv()  # to load the variables added in the .env file for local


# genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# os.environ["GOOGLE_API_KEY"] = st.secrets.db_credentials.GOOGLE_API_KEY

genai.configure(api_key=st.secrets.llm_credentials.GOOGLE_API_KEY)


def response_gemini(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text


def sql_retrieve(sql):
    ### add your database connection here
    db = mysql.connector.connect(
        # user=<user>,
        # password=<password>,
        # host=<host>,
        # port=<port>,
        # database= <database>
    )
    cursor = db.cursor()
    cursor.execute(sql)
    output = cursor.fetchall()

    cursor.close()
    db.close()

    return output


prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name `housing_prices` and has the following columns - "House_Name", "Location", "Municipality", "House_type", "Release_form", "Living_area", "Plot_area", "Other_area", "Rooms", "Balcony", "Floor", "Total_no_Floors", "Lift", "Built_on", "Charge", "Operating_cost", "Sold_date", "Starting_price", "Price_Change", "Final_Price"

    For example,
Example 1 - How many entries of records are present?,
the SQL command will be something like this: SELECT COUNT(*) FROM housing_prices;

Example 2 - List all houses located in Stockholm?,
the SQL command will be something like this: SELECT * FROM housing_prices WHERE Location='Stockholm';

Example 3 - What is the average living area of houses?,
the SQL command will be something like this: SELECT AVG(Living_area) FROM housing_prices;

Example 4 - Find all houses with more than 4 rooms?,
the SQL command will be something like this: SELECT * FROM housing_prices WHERE Rooms > 4;

Example 5 - What is the total operating cost of all houses?,
the SQL command will be something like this: SELECT SUM(Operating_cost) FROM housing_prices;

Example 6 - List the final prices of houses sold in 2023?,
the SQL command will be something like this: SELECT Final_Price FROM housing_prices WHERE Sold_date LIKE '2023%';

Example 7 - Find all houses that have a balcony?,
the SQL command will be something like this: SELECT * FROM housing_prices WHERE Balcony = 'Yes';

Also use "group by" when needed due to this issue:  In aggregated query without GROUP BY, expression #1 of SELECT list contains nonaggregated column 'sweden_property.housing_prices.House_Name'; this is incompatible with sql_mode=only_full_group_by

    
    Please ensure the SQL code does not have ``` at the beginning or end, and the word "sql" is not in the output.
    """
]


# Streamlit app
st.markdown(
    """
    <style>
    .main {
        background-color: black;
        color: green;
    }
    .stButton button {
        background-color: green;
        color: black;
    }
    .stTextInput div div input {
        background-color: black;
        color: green;
    }
    .stCheckbox div div div div input {
        accent-color: green;
    }
    .stTextArea textarea {
        background-color: black;
        color: green;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sweden Property data from Hemnet 🏠")

# Input form
question = st.text_input("Ask your question:")


if st.button("Submit"):
    if question:
        # Generate SQL query
        sql_query = response_gemini(question, prompt).strip()
        st.write("Generated SQL Query:")
        st.code(sql_query, language='sql')

        # Retrieve and display data
        try:
            results = sql_retrieve(sql_query)
            st.write("Query Results:")
            if results:
                for row in results:
                    st.write(row)
            else:
                st.write("No results found.")
        except Exception as e:
            st.write(f"Error: {e}")

if st.checkbox("Show prompt"):
    st.write(prompt[0])

st.markdown("""
    **Disclaimer:** The LLM is proficient at querying the database. However, it's advisable to familiarize yourself with the column names in the data before posing questions, particularly for complex queries. This understanding will help you frame your questions more effectively. For additional details about the data, please refer to this blog.
""")
