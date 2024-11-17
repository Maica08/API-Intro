import unittest
from unittest.mock import patch
import json
from app import app
from flask_mysqldb import MySQLdb

class BookListAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.mysql_patcher = unittest.mock.patch('app.mysql')
        self.mock_mysql = self.mysql_patcher.start()
        self.mock_cursor = self.mock_mysql.connection.cursor.return_value

    def tearDown(self):
        self.mysql_patcher.stop()

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Welcome to Book List!')

    def test_get_books(self):
        self.mock_cursor.fetchall.return_value = [
            (1, 'Book 1', 'Author 1', 2001),
            (2, 'Book 2', 'Author 2', 2002)
        ]
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 2)

    def test_get_book(self):
        self.mock_cursor.fetchone.return_value = (1, 'Book 1', 'Author 1', 2001)
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['data']['title'], 'Book 1')

    def test_get_book_not_found(self):
        self.mock_cursor.fetchone.return_value = None
        response = self.app.get('/books/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_create_book(self):
        response = self.app.post('/books', data=json.dumps({
            'title': 'New Book', 'author': 'New Author', 'year': 2020
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)

    def test_create_book_bad_request(self):
        response = self.app.post('/books', data=json.dumps({
            'title': 'New Book', 'author': 'New Author'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_update_book(self):
        self.mock_cursor.rowcount = 1
        response = self.app.put('/books/1', data=json.dumps({
            'title': 'Updated Book', 'author': 'Updated Author', 'year': 2021
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)

    def test_update_book_not_found(self):
        self.mock_cursor.rowcount = 0
        response = self.app.put('/books/999', data=json.dumps({
            'title': 'Updated Book', 'author': 'Updated Author', 'year': 2021
        }), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_delete_book(self):
        self.mock_cursor.rowcount = 1
        response = self.app.delete('/books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)

    def test_delete_book_not_found(self):
        self.mock_cursor.rowcount = 0
        response = self.app.delete('/books/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

if __name__ == '__main__':
    unittest.main()
