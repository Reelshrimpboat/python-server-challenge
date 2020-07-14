import psycopg2
from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


try:
   connection = psycopg2.connect(user="sysadmin",
                                 password="pynative@#29",
                                 host="127.0.0.1",
                                 port="5432",
                                 database="weekend_to_do_app")
   cursor = connection.cursor()
   postgreSQL_select_Query = "select * from task"

   cursor.execute(postgreSQL_select_Query)
   print("Selecting rows from mobile table using cursor.fetchall")
   mobile_records = cursor.fetchall()

   print("Print each row and it's columns values")
   for row in mobile_records:
       print("Id = ", row[0], )
       print("Model = ", row[1])
       print("Price  = ", row[2], "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


# @app.route('/tasks', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     elif request.method == 'GET':
#         return do_the_login()
#     else:
#         return show_the_login_form()

# conn = psycopg2.connect("dbname=weekend-to-do-app")
# cur = conn.cursor()

# cur.execute("SELECT * FROM tasks;")
# cur.fetchone()
