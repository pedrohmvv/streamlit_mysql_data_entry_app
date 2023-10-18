from banco_principal import Database  # Import the Database class from banco_principal.py
import streamlit as st

st.title("Connect to your desired MySQL database.")
st.subheader("Remember that you need to have authorized credencials to connect to the database.")

# Get user input for host, user, database name, and table name
host: str = st.text_input("Enter the host: ")
user: str = st.text_input("Enter the user: ")
sql_base: str = st.text_input("Enter the database you want to connect to: ")
table_name: str = st.text_input("Enter the table name: ")

# Create an instance of the Database class with the user input
database = Database(host, user, sql_base, table_name)

# Check if the database connection is successful
if database.connect():
    st.write("Connected!")
    database.input_data()  # Allow users to input data
    database.show_data()  # Shows the inputed data
    if st.button("Confirm"):
        database.insert_data()  # Insert data into the table
        database.show_table()  # Display the table
        if st.button("Stop"):
            database.disconnect()  # Disconnect from the database
