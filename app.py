from flask import Flask, request, jsonify # imports items from Flask for CRUD functions
app = Flask(__name__) # defines app as flask object
import psycopg2 # imports psycopg2 for database queries


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

# A route for homepage
@app.route('/')
def home():
    return '''<h1>Welcome Home</h1>
<p>Check out our books or take a stroll through our garden</p>'''


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

# A route ot return specific book, update specific book or specific delete
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

# # alternate GET that calls for a single book, saving for reference
# @app.route('/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)



@app.route("/garden", methods=['GET'])
def garden():
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
        list = []
        for row in plants:
            list.append(row[1])
            # print("id = ", row[0], )
            # print("plant = ", row[1])
        print("list = ", list)
        return jsonify(list)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
