from flask import Flask, request, jsonify # imports items from Flask for CRUD functions
app = Flask(__name__) # defines app as flask object
import psycopg2 # imports psycopg2 for database queries

# A route for homepage
@app.route('/')
def home():
    return '''<h1>Welcome to the Outdoor Library</h1>
<p>Check out our books or take a stroll through our garden</p>'''



# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'published': '1975'}
]


# ROUTES for BOOKS
# A route to return all of the available entries in our catalog or to POST a new entry
@app.route('/books', methods=['GET', 'POST'])
def book_route():
    if request.method == 'GET':  # checks method to see if GET
        return jsonify(books) # returns all books once gotten
    elif request.method == 'POST': # checks method to see if POST
        book = request.get_json() # sets book as incoming JSON object
        print("book: ", book) # prints book to console
        books.append(book) # appends book to book list
        return {'id': len(books)}, 200 #returns current number of books in list to show update
# END ROUTE for books GET ALL and POST 

# A route to return specific book, update specific book or specific delete
@app.route('/books/<int:index>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_route(index):
    if request.method == 'GET':  # checks method to see if GET
        return jsonify(books[index]), 200 #returns specified book
    elif request.method == 'PUT': # checks method to see if PUT
        book = request.get_json() # sets book as incoming JSON object
        books[index] = book # changes data in index position of books list
        return jsonify(books[index]), 200 #returns data of updated book
    elif request.method == 'DELETE': # checks method to see if DELETE
        books.pop(index) # removes book at index from list
        return "Aaannnnnnnd it's gone", 200 # sends back south park joke to show book has been removed
#END ROUTE foir GET INDIVIDUAL, PUT, and DELETE

# Test object for POSTMAN books requests, use in Body tab, raw format, as JSON object
# {
#     "id": 3,
#     "title": "A Book With Me In It",
#     "author": "Me",
#     "published": "2008"
# }

# END ROUTES Ffor BOOKS

# ROUTES for GARDEN DATABASE - PLANT TABLE
# GET ROUTE for PLANT TABLE
@app.route("/garden", methods=['GET'])
def garden_get():
    #  GET occurs here:
    try:
        # connect to database
        connection = psycopg2.connect(
                                        host="localhost",
                                        port="5432",
                                        database="garden"
                                        )
        cursor = connection.cursor()  # create cursor to interact with database

        get_query = "select * from plant" # defines query for GET request

        cursor.execute(get_query) # sends query to the database
        print("Selecting rows from plants") # logs that query has been sent to database
        
        plants = cursor.fetchall() # defines list 'plants' as what returns from database
        print("plants: " , plants) # logs what was defined in plants
        
        return jsonify(plants) # returns data as JSON string

    except (Exception, psycopg2.Error) as error:  # error catching
        print("Error while fetching data from PostgreSQL", error) # logs error

    # ending tag/ to do after error
    finally:
        if(connection):  # if for when connection remains open
            cursor.close() # closes cursor
            connection.close() # closes database connection
            print("PostgreSQL connection is closed") # logs that connection is closed
# END GET ROUTE for PLANT TABLE

# POST ROUTE for PLANT TABLE
@app.route("/garden", methods=['POST'])
def garden_post():
    #  POST occurs here:
    try:
        plant = request.get_json()  # sets plant as incoming JSON object

        # connect to database
        connection = psycopg2.connect(
                                            host="localhost",
                                            port="5432",
                                            database="garden"
                                            )
        cursor = connection.cursor() # create cursor to interact with database

        # defines database query
        post_query = '''INSERT INTO "plant" ("name", "kingdom", "clade", "order", "family", "subfamily", "genus")
            VALUES(%s, %s, %s, %s, %s, %s, %s);'''

        # defines converts values from plant into query value input
        post_values = (plant["name"], plant["kingdom"], plant["clade"], plant["order"], plant["family"], plant["subfamily"], plant["genus"])
        print('post query:', post_query , " : post_values:" , post_values) # log to check query and values
        
        cursor.execute(post_query, post_values) # sends query and values to database
        connection.commit()# commits query to database
        
        return ("Record inserted successfully into garden table", 200) # move to next action and return success message to server


    
    except (Exception, psycopg2.Error) as error: # error catching
        print("Error while fetching data from PostgreSQL", error) # log error


    # ending tag/ to do after error
    finally:
        if(connection): # if for when connection remains open
            cursor.close() # closes cursor
            connection.close() # closes database connection
            print("PostgreSQL connection is closed") # logs that connection is closed
            garden_get() # runs GET to update with new values
# END POST ROUTE for PLANT TABLE

# Test object for POSTMAN garden requests, use in Body tab, raw format, as JSON object
# {
#     "name": "Rose",
#     "kingdom": "Plantae",
#     "clade": "Angiosperms",
#     "order": "Rosales",
#     "family": "Rosaceae",
#     "subfamily": "Rosoideae",
#     "genus": "Rosa"
# }

# END ROUTES for PLANT TABLE
