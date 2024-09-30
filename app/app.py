from flask import Flask, render_template, request
import requests
import json
import os
import psycopg2
from datetime import datetime


app = Flask(__name__)


@app.route('/')
#this method renders an html file located in the AppDirect/app/templates directory.
def index():
    
    return render_template("index.html")

@app.route('/test')
# this was simply a test to see how to display a message by using a different route.
def test():
   
    return "This is the test to see what appens\\\"

@app.route('/sql-check')
def checkDB():

    #This method tries to connect to the default Postgres database and gets a list of databases - can be used to verify that the database exists
    conn = None
    try:
        conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host='postgresql-service', port= '5432')
        message_to_display = "Connectend to Database <br>"
    except Exception as e:
        message_to_display = "There was a problem connecting to the database <br>" + str(e)
    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database;")
        database_list = cur.fetchall()
        message_to_display += "The following databases are on the list <br>"
        for database in database_list:
            message_to_display += str(database) + "<br>"        
        cur.close()
        conn.close()    
    return message_to_display
@app.route('/sql-create')
def createDB():
    #This method will create the database and table
    message_to_display = ""
    conn = None
    db_exists = False
    # Let's first connect
    try:
        conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host='postgresql-service', port= '5432')
        message_to_display = "Connectend to postgres default database <br>"
        message_to_display += "Checking to see if AppDirect database exists... <br>"
    except Exception as e: 
        message_to_display += "There as an error connecting to the default postgres database <br>" + str(e)
    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()   
        try:
            cur.execute("CREATE database appdirectdb")
            message_to_display += "database created! ...will now try to create the table <br>"
            
            cur.close()
            conn.close()
            conn = None
            conn = psycopg2.connect(database="appdirectdb", user='postgres', password='postgres', host='postgresql-service', port= '5432')
            if conn is not None:
                conn.autocommit = True
                cur = conn.cursor()
                message_to_display += "Conneted to the App Direct DB... <br>"
                cur.execute("""CREATE TABLE tblrecords (data VARCHAR(250))""")
                message_to_display += "Created Table without any errors"
                cur.close()
                conn.close()
            else:
                message_to_display += "There was a problem creatig the table <br>"
        except Exception as e:
            message_to_display += "There was an error creating the datbase: <br>" + str(e)
        conn.close()

    return message_to_display

@app.route('/sql-add')
def addData():            
    try:
        conn = psycopg2.connect(database="appdirectdb", user='postgres', password='postgres', host='postgresql-service', port= '5432')
        message_to_display = "Connectend to Database <br>"
    except Exception as e:
        message_to_display = "Unable to connect to the Database. Try browsing /sql-check to see if the Database exists <br>" + str(e)
    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()
        try:
            # sql_statemnt = """INSERT INTO tblRecords (Data) VALUES (%s)"""
            #sql_values = "hello this is a test"
            sql_values = str(datetime.now())
            cur.execute("INSERT INTO tblrecords VALUES ('" + sql_values +"')")
            # cur.execute(sql_statemnt, sql_values)
            message_to_display += "Added a record to the table without any errors <br>"
            cur.close()
        except Exception as e:
            message_to_display += " There was an error:" + str(e)
           
        conn.close()

    return message_to_display
@app.route('/sql-show')
def showData():            
    try:
        conn = psycopg2.connect(database="appdirectdb", user='postgres', password='postgres', host='postgresql-service', port= '5432')
        message_to_display = "Connectend to Database <br>"
    except Exception as e:
        message_to_display = "Unable to connect to the Database. Try browsing /sql-check to see if the Database exists <br>" + str(e)
    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()
        try:            
            query_result = cur.execute("SELECT * from tblrecords")
            message_to_display += str(query_result)
            cur.close()
        except Exception as e:
            message_to_display += " There was an error:" + str(e)
           
        conn.close()

    return message_to_display
@app.route('/support')
# This creates a file and dumps all environment variables. Used as an example of creating a file for support to troubleshoot.
def create_support_file():
    file_path = 'app/'
    file_name = 'env_vars.txt'
    file_name_w_path = os.path.join(file_path, file_name)
    
    file_to_write = open(file_name_w_path, "w")
    file_content = os.environ
    file_content_str = str(file_content)
    file_to_write.write(file_content_str)
    file_to_write.close()
    return "Check the App directory for a file called env_var.txt"



@app.route('/msg')
# This displays a message that can be passed as an evironment variable PAGE_MESSAGE
def display_message():
    message_to_display = os.environ["PAGE_MESSAGE"]
    return message_to_display

@app.route('/license-check')
def license_check():
    message_to_display = ""
    return message_to_display

if __name__ == '__main__':
    app.run(host='0.0.0.0')
