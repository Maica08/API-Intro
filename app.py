from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from http import HTTPStatus

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'book_list'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Welcome to Book List!'

@app.route('/books', methods=['GET'])
def get_books():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM books''')
        data = cur.fetchall()
        cur.close()
        books = [{'id': row[0], 'title': row[1], 'author': row[2], 'year': row[3]} for row in data]
        return jsonify({'success': True, 'data': books, 'total': len(books)}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM books WHERE idbooks = %s''', (book_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            book = {'id': row[0], 'title': row[1], 'author': row[2], 'year': row[3]}
            return jsonify({'success': True, 'data': book}), HTTPStatus.OK
        return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


# NOTE: idbooks is being incremented automatically
@app.route('/books', methods=['POST'])
def create_book():
    try:
        if not request.json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST
        
        data = request.json
        title = data.get('title')
        author = data.get('author')
        year = data.get('year')

        if not title or not author or not year:
            return jsonify({'success': False, 'error': 'All fields (title, author, year) are required'}), HTTPStatus.BAD_REQUEST

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO books (title, author, year) VALUES (%s, %s, %s)''', (title, author, year))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True, 'message': 'Book added successfully'}), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_data(book_id):
    try:
        if not request.json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST
        
        data = request.json
        title = data.get('title')
        author = data.get('author')
        year = data.get('year')

        if not title or not author or not year:
            return jsonify({'success': False, 'error': 'All fields (title, author, year) are required'}), HTTPStatus.BAD_REQUEST

        cur = mysql.connection.cursor()
        cur.execute('''UPDATE books SET title = %s, author = %s, year = %s WHERE idbooks = %s''', 
                    (title, author, year, book_id))
        mysql.connection.commit()
        cur.close()

        if cur.rowcount == 0:
            return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

        return jsonify({'success': True, 'message': 'Book updated successfully'}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_data(book_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM books WHERE idbooks = %s''', (book_id,))
        mysql.connection.commit()
        cur.close()

        if cur.rowcount == 0:
            return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

        return jsonify({'success': True, 'message': 'Book deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)
