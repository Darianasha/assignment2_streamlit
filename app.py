import pandas as pd
import streamlit as st
import sqlalchemy as sa
from sqlalchemy import text




st.set_page_config(
    layout="centered", page_icon="💕", page_title="Daria Gole - Assignment 2"
)



# Connect to the database
engine = sa.create_engine("postgresql://postgres:M!v#3vKDd46hnCV@db.dprpqkfckvlgjxzifnkq.supabase.co:5432/postgres")

tables = (
    "DiseaseType", "Country", "Disease", "Discover", "Users", "PublicServant", 
    "Doctor", "Specialize", "Record"
)

#write a header -- works
st.title("Daria Gole - CSCI 241 Assignment 2. An application with CRUD operations")

st.write("First, select a table to view data from it:")

table = st.selectbox("", tables)

# Function to retrieve data from the database
def get_data(table):
    with engine.connect() as conn:
        query = text(f"SELECT * FROM assignment2.{table}")
        df = pd.read_sql(query, conn)
        return df  


st.dataframe(get_data(table))


# Function to insert data into the database -- works
def insert_data(table, values_str):
    with engine.connect() as conn:
        query = text(f"INSERT INTO assignment2.{table} VALUES ({values_str})")
        conn.execute(query)

# function to get the names of countries from a column -- works
def get_countries(table, column):
    with engine.connect() as conn:
        query = text(f"SELECT DISTINCT {column} FROM assignment2.{table}")
        df = pd.read_sql(query, conn)
        return df

#function to get the id of disease type -- works
def get_disease_type_id():
    with engine.connect() as conn:
        query = text(f"SELECT id FROM assignment2.diseasetype")
        df = pd.read_sql(query, conn)
        return df

#function to get the disease code -- works
def get_disease_code():
    with engine.connect() as conn:
        query = text(f"SELECT diseasecode FROM assignment2.disease")
        df = pd.read_sql(query, conn)
        return df

#function to get the email of users -- works
def get_users_email():
    with engine.connect() as conn:
        query = text(f"SELECT email FROM assignment2.users")
        df = pd.read_sql(query, conn)
        return df


#collect data from user -- works
def collect_data(table):
    if table == "Users":
        email = st.text_input("Enter email")
        name = st.text_input("Enter name")
        surname =   st.text_input("Enter surname")
        salary = st.number_input("Enter salary")
        phone = st.text_input("Enter phone")
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        values_str = f"'{email}', '{name}', '{surname}', {salary}, '{phone}', '{cname}'"
        return values_str
    if table == "DiseaseType":
        id = st.number_input("Enter id")
        description = st.text_input("Enter description")
        values_str = f"{id}, '{description}'"
        return values_str
    if table == "Country":
        cname = st.text_input("Enter country name")
        population = st.number_input("Enter population")
        values_str = f"'{cname}', {population}"
        return values_str
    if table == "Disease":
        diseasecode = st.text_input("Enter disease code")
        pathogen = st.text_input("Enter pathogen")
        description = st.text_input("Enter description")
        id = st.selectbox("Select disease type id", get_disease_type_id())
        values_str = f"'{diseasecode}', '{pathogen}', '{description}', {id}"
        return values_str
    if table == "Discover":
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        firstencdate = st.date_input("Enter date (first encountered")
        values_str = f"'{cname}', '{diseasecode}', '{firstencdate}'"
        return values_str
    if table == "PublicServant":
        email = st.selectbox("Select user email", get_users_email())
        department = st.text_input("Enter department")
        values_str = f"'{email}', '{department}'"
        return values_str
    if table == "Doctor":
        email = st.selectbox("Select user email", get_users_email())
        degree = st.text_input("Enter degree")
        values_str = f"'{email}', '{degree}'"
        return values_str
    if table == "Specialize":
        id = st.selectbox("Select disease type id", get_disease_type_id())
        email = st.selectbox("Select user email", get_users_email())
        values_str = f"{id}, '{email}'"
        return values_str
    if table == "Record":
        email = st.selectbox("Select user email", get_users_email())
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        totaldeaths = st.number_input("Enter num of total deaths")
        totalpatients = st.number_input("Enter num of total patients")
        values_str = f"'{email}', '{cname}', '{diseasecode}', {totaldeaths}, {totalpatients}"
        return values_str

#write text to the user -- works
st.write("Now, you can insert data into the table. Enter the values and click the button below.")


# streamlit form to insert a record -- works
with st.form("insert_form"):
    st.write("Create a new record")
    values_str = collect_data(table)
    submit_button = st.form_submit_button(label="Insert")
    if submit_button:
        insert_data(table, values_str)

# write a text to the user -- works
st.write("Update a record from the table. Enter the values and click the button below.")


# streamlit form to update a record -- works
with st.form("update_form"):
    st.write("Update an existing record")
    if table == "Users":
        email = st.selectbox("Select email", get_users_email())
        name = st.text_input("Enter new name")
        surname =   st.text_input("Enter new surname")
        salary = st.number_input("Enter new salary")
        phone = st.text_input("Enter new phone")
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        query = text(f"UPDATE assignment2.{table} SET name = '{name}', surname = '{surname}', salary = {salary}, phone = '{phone}', cname = '{cname}' WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "DiseaseType":
        id = st.selectbox("Select id", get_disease_type_id())
        description = st.text_input("Enter description")
        query = text(f"UPDATE assignment2.{table} SET description = '{description}' WHERE id = {id}")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Country":
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        population = st.number_input("Enter population")
        query = text(f"UPDATE assignment2.{table} SET population = {population} WHERE cname = '{cname}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Disease":
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        pathogen = st.text_input("Enter new pathogen")
        description = st.text_input("Enter new description")
        id = st.selectbox("Select disease type id", get_disease_type_id())
        query = text(f"UPDATE assignment2.{table} SET pathogen = '{pathogen}', description = '{description}', id = {id} WHERE diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Discover":
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        firstencdate = st.date_input("Enter date (first encountered")
        query = text(f"UPDATE assignment2.{table} SET firstencdate = '{firstencdate}' WHERE cname = '{cname}' AND diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "PublicServant":
        email = st.selectbox("Select user email", get_users_email())
        department = st.text_input("Enter new department")
        query = text(f"UPDATE assignment2.{table} SET department = '{department}' WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Doctor":
        email = st.selectbox("Select user email", get_users_email())
        degree = st.text_input("Enter new degree")
        query = text(f"UPDATE assignment2.{table} SET degree = '{degree}' WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Specialize":
        #write a warning that the user can't update the table
        st.write("You can't update this table because it doesn't have non-key attributes")
        submit_button = st.form_submit_button(label="Click")
        if submit_button:
            #ask the user to stop clicking
            st.write("Stop clicking")

    if table == "Record":
        email = st.selectbox("Select user email", get_users_email())
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        totaldeaths = st.number_input("Enter new num of total deaths")
        totalpatients = st.number_input("Enter new num of total patients")
        query = text(f"UPDATE assignment2.{table} SET totaldeaths = {totaldeaths}, totalpatients = {totalpatients} WHERE email = '{email}' AND cname = '{cname}' AND diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)


# write a text to the user -- works
st.write("Delete a record from the table. Enter the values and click the button below.")


# streamlit form to delete a record -- works
with st.form("delete_form"):
    st.write("Delete an existing record")
    if table == "Users":
        email = st.selectbox("Select email", get_users_email())
        query = text(f"DELETE FROM assignment2.{table} WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "DiseaseType":
        id = st.selectbox("Select id", get_disease_type_id())
        query = text(f"DELETE FROM assignment2.{table} WHERE id = {id}")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Country":
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        query = text(f"DELETE FROM assignment2.{table} WHERE cname = '{cname}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Disease":
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        query = text(f"DELETE FROM assignment2.{table} WHERE diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Discover":
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        query = text(f"DELETE FROM assignment2.{table} WHERE cname = '{cname}' AND diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "PublicServant":
        email = st.selectbox("Select user email", get_users_email())
        query = text(f"DELETE FROM assignment2.{table} WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Doctor":
        email = st.selectbox("Select user email", get_users_email())
        query = text(f"DELETE FROM assignment2.{table} WHERE email = '{email}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Specialize":
        email = st.selectbox("Select user email", get_users_email())
        id = st.selectbox("Select disease type id", get_disease_type_id())
        query = text(f"DELETE FROM assignment2.{table} WHERE email = '{email}' AND id = {id}")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    if table == "Record":
        email = st.selectbox("Select user email", get_users_email())
        cname = st.selectbox("Select country", get_countries("country", "cname"))
        diseasecode = st.selectbox("Select disease code", get_disease_code())
        query = text(f"DELETE FROM assignment2.{table} WHERE email = '{email}' AND cname = '{cname}' AND diseasecode = '{diseasecode}'")
        submit_button = st.form_submit_button(label="Delete")
        if submit_button:
            with engine.connect() as conn:
                conn.execute(query)
    

    



        






