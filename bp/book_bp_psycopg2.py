from flask import Blueprint, request, jsonify
import psycopg2

book_bp = Blueprint('book_bp_psycopg2', __name__, url_prefix='/books')

def get_db_connection():
    conn = psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="1111",
        host="localhost"
    )
    return conn

@book_bp.route('/', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book;')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)

@book_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO book (title, author, language, published_date) VALUES (%s, %s, %s, %s) RETURNING id;',
        (data.get("title"), data.get("author"), data.get("language"), data.get("published_date"))
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    new_book = {
        "id": new_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "language": data.get("language"),
        "published_date": data.get("published_date")
    }
    return jsonify(new_book), 201
@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book WHERE id = %s;', (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    book_dict = {
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "language": book[3],
        "published_date": book[4]
    }
    return jsonify(book_dict)
@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE book SET title = %s, author = %s, language = %s, published_date = %s WHERE id = %s;',
        (data.get("title"), data.get("author"), data.get("language"), data.get("published_date"), book_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Book updated successfully"})

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM book WHERE id = %s;', (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Book deleted successfully: {book_id}"})