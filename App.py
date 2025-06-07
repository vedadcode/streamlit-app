import streamlit as st
import pandas as pd
import datetime

# Function to check login
def login(username, password):
    return username == "admin" and password == "password"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'App Name', 'Test Result', 'Comments', 'Tested By', 'Failure Reason', 'Common Issues'])

# Main app logic
if st.session_state.logged_in:
    # Function to add a new test entry
    def add_test_entry(date, time, app_name, test_result, comments, tested_by, failure_reason=None, common_issues=None):
        new_entry = pd.DataFrame({
            'Date': [date],
            'Time': [time],
            'App Name': [app_name],
            'Test Result': [test_result],
            'Comments': [comments],
            'Tested By': [tested_by],
            'Failure Reason': [failure_reason],
            'Common Issues': [common_issues]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)

    # Title of the app
    st.markdown("""
        <style>
            body {
                background-color: #f0f4f8;
                font-family: 'Arial', sans-serif;
            }
            .title {
                text-align: center;
                font-size: 2.5em;
                color: #4CAF50;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .header {
                text-align: center;
                color: #2196F3;
                font-size: 1.8em;
                margin-bottom: 20px;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            }
            .form-container {
                background-color: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                padding: 30px;
                margin: 20px auto;
                max-width: 600px;
            }
            .dataframe {
                border-radius: 10px;
                overflow: hidden;
                margin-top: 20px;
            }
            .dataframe th {
                background-color: #4CAF50;
                color: white;
            }
            .dataframe td {
                background-color: #f9f9f9;
            }
            .button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>🎉 Daily App Testing Dashboard 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='header'>Update Test Results</h3>", unsafe_allow_html=True)

    # Update form
    with st.form(key='test_form', clear_on_submit=True):
        date = st.date_input('Date', value=datetime.date.today(), disabled=True)
        time = st.time_input('Time', value=datetime.datetime.now().time(), disabled=False)  # Pre-filled with current time
        
        # Dropdown for App Name
        app_name = st.selectbox('App Name', ['Rummy Rani', 'Go Rummy', 'Sky Rummy', '52 Cards'])
        
        test_result = st.selectbox('Test Result', ['Pass', 'Fail'])
        comments = st.text_area('Comments', placeholder="Enter any additional comments here...")
        tested_by = st.text_input('Tested By', placeholder='Enter your name')

        # Dropdown for common issues
        common_issues = st.selectbox(
            'Common Issues',
            [
                'None',
                'Server Delay',
                'Gameplay Bugs',
                'UI Glitches',
                'Connection Drops',
                'Payment Issues',
                'Other'
            ],
            index=0  # Default selection
        )

        # Submit button
        submit_button = st.form_submit_button(label='Submit', help="Click to submit the test results")

        if submit_button:
            # Add the test entry with the selected values
            add_test_entry(date, time, app_name, test_result, comments, tested_by, common_issues=common_issues)
            st.success('Test result added!')

    # Display the testing sheet
    st.header('📊 Testing Results 📊')
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data.style.set_table_attributes('class="dataframe"').set_properties(**{
            'border-radius': '10px',
            'overflow': 'hidden'
        }))
    else:
        st.write("No data available yet.")

    # Logout option
    if st.button("Logout", help="Click to log out"):
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
else:
    # Login form
    st.markdown("""
        <style>
            .login-title {
                text-align: center;
                font-size: 2em;
                color: #4CAF50;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='login-title'>🔐 Login</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Welcome to the Testing Dashboard</h2>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully! Please refresh the page to continue.")
        else:
            st.error("Invalid username or password.")
