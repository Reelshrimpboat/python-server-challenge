import psycopg2
from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


try:
   connection = psycopg2.connect(
                                 host="localhost",
                                 port="5432",
                                 database="garden")
   cursor = connection.cursor()
   postgreSQL_select_Query = "select * from plant"

   cursor.execute(postgreSQL_select_Query)
   print("Selecting rows from plants")
   plants = cursor.fetchall()

   print("Print each row and it's columns values")
   for row in plants:
       print("id = ", row[0], )
       print("plant = ", row[1])

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
