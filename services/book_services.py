from logger.logger_base import log
from flask import jsonify

class BookService:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_all_books(self):
        try:
            self.books = list(self.db_connector.db.books.find())
            return self.books
        except Exception as e:
            log.critical(f'Error fetching all books from the database: {e}')
            return jsonify({'error': f'Error fetching all books from the database: {e}'}), 500
        
    def get_book_by_id(self, book_id):
        try:
            self.book = self.db_connector.db.books.find_one({'_id': book_id})
            return self.book
        except Exception as e:
            log.critical(f'Error fetching the book id from the database: {e}')
            return jsonify({'error': f'Error fetching the book id from the database: {e}'}), 500
        
    def add_book(self, new_book):
        try:
            self.max_id = self.db_connector.db.books.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.books.count_documents({}) > 0 else 0
            self.new_id = self.max_id + 1
            new_book['_id'] = self.new_id
            self.db_connector.db.books.insert_one(new_book)
            return new_book
        except Exception as e:
            log.critical(f'Error creating the new book: {e}')
            return jsonify({'error': f'Error creating the new book: {e}'}), 500
        
    def update_book(self, book_id, updated_data):
        try:
            updated_book = self.get_book_by_id(book_id)
            if updated_book:
                result = self.db_connector.db.books.update_one({'_id': book_id}, {'$set': updated_data})
                if result.modified_count > 0:
                    return updated_book
                else:
                    return {'message': 'The book is already up-to-date'}
            else:
                return None

        except Exception as e:
            log.critical(f'Error updating the book data: {e}')
            return jsonify({'error': f'Error updating the book data: {e}'}), 500
        
    def delete_book(self, book_id):
        try:
            deleted_book = self.get_book_by_id(book_id)
            if deleted_book:
                self.db_connector.db.books.delete_one({'_id': book_id})
                return deleted_book
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the book data: {e}')
            return jsonify({'error': f'Error deleting the book data: {e}'}), 500