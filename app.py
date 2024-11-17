from flask import Flask, jsonify, request
from http import HTTPStatus


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

books = [
    {
        'id': 1,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'year': 1957
    },
    {
        'id': 2,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J.K. Rowling',
        'year': 1997
    }
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'success': True, 'data': books, 'total': len(books)}), HTTPStatus.OK

def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify({'success': True, 'data': book}), HTTPStatus.OK
    return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

@app.route('/books', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST
    data = request.json
    #validation
    required_fields = ['title', 'author', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'{field} is required'}), HTTPStatus.BAD_REQUEST
    new_book = {
        'id': books[-1]['id'] + 1,
        'title': data['title'],
        'author': data['author'],
        'year': data['year']
    }
    books.append(new_book)
    return jsonify({'success': True, 'data': new_book}), HTTPStatus.CREATED

if __name__ == '__main__':
    app.run(debug=True)