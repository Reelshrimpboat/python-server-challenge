from flask import Flask, request, jsonify
app = Flask(__name__)
import psycopg2


# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome Home</h1>
<p>Check out our books or take a stroll through our garden</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/books', methods=['GET', 'POST'])
def book_route():
    if request.method == 'GET':
        return jsonify(books)
    elif request.method == 'POST':
        book = request.get_json()
        print("book: ", book)
        books.append(book)
        return {'id': len(books)}, 200

# # GET that calls for a single book
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
