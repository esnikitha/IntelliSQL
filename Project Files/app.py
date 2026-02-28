import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

prompt = """
You are an expert in converting English questions into SQL queries.

The SQL database name is STUDENTS.
The table has the following columns:
NAME, CLASS, MARKS, COMPANY.

Important:
- Return ONLY the SQL query.
- Do NOT include explanations.
- Do NOT include ``` or the word SQL.
- The query must be valid SQLite syntax.

Examples:

Example 1:
How many entries of records are present?
SQL:
SELECT COUNT(*) FROM STUDENTS;

Example 2:
Tell me all students studying in MCom class.
SQL:
SELECT * FROM STUDENTS WHERE CLASS = 'MCom';

Now convert the following question into SQL:
"""

def get_response(question):
    full_prompt = prompt + question
    response = model.generate_content(full_prompt)
    return response.text.strip()

def read_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.close()
    return rows

def page_home():
    st.markdown("""
        <style>
        body {
            background-color: #2E2E2E;
        }
        .main-title {
            text-align: center;
            color: #4CAF50;
            font-size: 2.5em;
        }
        .sub-title {
            text-align: center;
            color: #4CAF50;
            font-size: 1.5em;
        }
        .offerings {
            padding: 20px;
            color: white;
        }
        .offerings h2 {
            color: #4CAF50;
        }
        .offerings ul {
            list-style-type: none;
            padding: 0;
        }
        .offerings li {
            margin: 10px 0;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Welcome to IntelliSQL</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Revolutionizing Database Querying with Advanced LLM Capabilities</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            "https://cdn1.iconfinder.com/data/icons/business-dual-color-glyph-set-3/128/Data_warehouse-1024.png",
            use_column_width=True
        )

    with col2:
        st.markdown("""
            <div class='offerings'>
                <h2>Wide Range of Offerings</h2>
                <ul>
                    <li>✨ Intelligent Query Assistance</li>
                    <li>📊 Data Exploration and Insights</li>
                    <li>📈 Efficient Data Retrieval</li>
                    <li>🚀 Performance Optimization</li>
                    <li>🛠 Syntax Suggestions</li>
                    <li>📉 Trend Analysis</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def page_about():
    st.markdown("""
        <style>
        .about-container {
            color: white;
            padding: 20px;
            font-size: 18px;
        }
        .about-title {
            text-align: center;
            color: #4CAF50;
            font-size: 2em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='about-title'>About IntelliSQL</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div class='about-container'>
            <p>
            IntelliSQL is an innovative project aimed at revolutionizing database querying 
            using advanced Large Language Model (LLM) capabilities.
            </p>

            <p>
            It enables users to convert natural language questions into SQL queries,
            making database interaction intuitive, intelligent, and efficient.
            </p>

            <p>
            The system integrates:
            </p>

            <ul>
                <li>🤖 Gemini Pro (LLM)</li>
                <li>🗄 SQLite Database</li>
                <li>🌐 Streamlit Web Interface</li>
                <li>☁ Cloud-Ready Architecture</li>
            </ul>

            <p>
            IntelliSQL bridges the gap between human language and structured database systems,
            empowering both beginners and professionals.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://download.logo.wine/logo/Oracle_SQL_Developer/Oracle_SQL_Developer-Logo.wine.png",
        use_column_width=True
    )

def page_intelligent_query_assistance():

    st.markdown("""
        <style>
        .tool-input {
            margin-bottom: 20px;
            color: white;
        }
        .response {
            margin-top: 20px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#4CAF50;'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)

    st.write("""
    IntelliSQL enhances database querying by converting natural language
    into executable SQL queries using Gemini Pro.
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='tool-input'>", unsafe_allow_html=True)

        que = st.text_input("Enter Your Query:")
        submit = st.button("Get Answer")

        st.markdown("</div>", unsafe_allow_html=True)

        if submit and que:

            try:
                # Step 1: Generate SQL from Gemini
                generated_sql = get_response(que)

                # Clean possible markdown formatting
                generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()

                st.subheader("Generated SQL Query:")
                st.code(generated_sql, language="sql")

                # Step 2: Execute SQL
                result = read_query(generated_sql, "data.db")

                st.markdown("<div class='response'>", unsafe_allow_html=True)
                st.subheader("Query Result:")

                if isinstance(result, str):
                    st.error(result)
                else:
                    st.table(result)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/9850/9850877.png",
            use_column_width=True
        )

def main():
    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="🤖",
        layout="wide"
    )

    # Sidebar Styling
    st.sidebar.title("Navigation")
    st.sidebar.markdown(
        """
        <style>
        .css-1d391kg {
            background-color: #2E2E2E;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    pages = {
        "Home": page_home,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
        "About": page_about
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()