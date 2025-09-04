from flask import Blueprint, request, jsonify
from db.users.connect_db import engine

book_bp_engine = Blueprint('book_bp_sqlalchemy', __name__, url_prefix='/books')

@book_bp_engine.route('/', methods=['GET'])
def get_books():
    with engine.connect() as conn:
        result = conn.execute('SELECT * FROM book order by id;')
        books = [dict(row) for row in result]
    return jsonify(books)

@book_bp_engine.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    with engine.connect() as conn:
        result = conn.execute(
            'INSERT INTO book (title, author, language, published_date) VALUES (%s, %s, %s, %s) RETURNING id;',
            (data.get("title"), data.get("author"), data.get("language"), data.get("published_date"))
        )
    new_id = result.fetchone()[0]
    new_book = {
        "id": new_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "language": data.get("language"),
        "published_date": data.get("published_date")
    }
    return jsonify(new_book), 201

@book_bp_engine.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    with engine.connect() as conn:
        result = conn.execute('SELECT * FROM book WHERE id = %s;', (book_id,))
        book = result.fetchone()
        if book is None:
            return jsonify({"error": "Book not found"}), 404
    book_dict = dict(book)
    return jsonify(book_dict)

@book_bp_engine.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    print(data)
    with engine.connect() as conn:
        conn.execute(
            'UPDATE book SET title = %s, author = %s, language = %s WHERE id = %s;',
            (data.get("title"), data.get("author"), data.get("language"), book_id)
        )
    return jsonify({"message": "Book updated successfully"})

@book_bp_engine.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    with engine.connect() as conn:
        result = conn.execute('SELECT * FROM book WHERE id = %s;', (book_id,))
        book = result.fetchone()
        if book is None:
            return jsonify({"error": "Book not found"}), 404
    with engine.connect() as conn:
        conn.execute('DELETE FROM book WHERE id = %s;', (book_id,))
    return jsonify({"message": f"Book deleted successfully: {book_id}"})