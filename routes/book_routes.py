from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class BookRoutes(Blueprint):
    def __init__(self, book_service, book_schema):
        super().__init__('book', __name__)
        self.book_service = book_service
        self.book_schema = book_schema
        self.register_routes()

    def register_routes(self):
        self.route('/api/books', methods=['GET'])(self.get_books)
        self.route('/api/books/<int:book_id>', methods=['GET'])(self.get_books_by_id)
        self.route('/api/books', methods=['POST'])(self.add_book)
        self.route('/api/books/<int:book_id>', methods=['PUT'])(self.update_book)
        self.route('/api/books/<int:book_id>', methods=['DELETE'])(self.delete_book)

    def get_books(self):
        try:
            self.books = self.book_service.get_all_books()
            return jsonify(self.books), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_books_by_id(self, book_id):
        self.book = self.book_service.get_book_by_id(book_id)
        if self.book:
            return jsonify(self.book), 200
        else: 
            return jsonify({'error': 'Book not found'}), 404
        
    def add_book(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')

            try:
                self.book_schema.validate_title(self.title)
                self.book_schema.validate_author(self.author)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.new_book = {
                'title': self.title,
                'author': self.author
            }

            self.created_book = self.book_service.add_book(self.new_book)
            return jsonify(self.created_book), 201
        except Exception as e:
            log.critical(f'Error adding a new book to the database: {e}')

    def update_book(self, book_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')

            try:
                self.book_schema.validate_title(self.title)
                self.book_schema.validate_author(self.author)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.book_updated = self.book_service.update_book(book_id, self.data)

            if self.book_updated:
                return jsonify(self.book_updated), 200
            else:
                return jsonify({'error': 'Book not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the book in the database: {e}')

    def delete_book(self, book_id):
        try:
            self.book_deleted = self.book_service.delete_book(book_id)
            if self.book_deleted:
                return jsonify(self.book_deleted), 200
            else:
                return jsonify({'error': 'Book not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the book in the database: {e}')
