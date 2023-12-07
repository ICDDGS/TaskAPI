from logger.logger_base import log
from flask import jsonify

class TaskServices:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def get_all_tasks(self):
        try:
            self.tasks = list(self.db_connector.db.tasks.find())
            return self.tasks
        except Exception as e:
            log.critical(f'Error fetching all tasks from the database: {e}')
            return jsonify({'error': f'Error fetching all tasks from the database: {e}'}), 500
        
    def get_task_by_id(self, task_id):
        try:
            self.task = self.db_connector.db.tasks.find_one({'_id': task_id})
            return self.task
        except Exception as e:
            log.critical(f'Error fetching the task id from the database: {e}')
            return jsonify({'error': f'Error fetching the task id from the database: {e}'}), 500
        
    def add_task(self, new_task):
        try:
            self.max_id = self.db_connector.db.tasks.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.tasks.count_documents({}) > 0 else 0
            self.new_id = self.max_id + 1
            new_task['_id'] = self.new_id
            self.db_connector.db.tasks.insert_one(new_task)
            return new_task
        except Exception as e:
            log.critical(f'Error creating the new task: {e}')
            return jsonify({'error': f'Error creating the new task: {e}'}), 500
        
    def update_task(self, task_id, updated_data):
        try:
            updated_task = self.get_task_by_id(task_id)
            if updated_task:
                result = self.db_connector.db.tasks.update_one({'_id': task_id}, {'$set': updated_data})
                if result.modified_count > 0:
                    return updated_task
                else:
                    return {'message': 'The task is already up-to-date'}
            else:
                return None

        except Exception as e:
            log.critical(f'Error updating the task data: {e}')
            return jsonify({'error': f'Error updating the task data: {e}'}), 500
        
    def delete_task(self, task_id):
        try:
            deleted_task = self.get_task_by_id(task_id)
            if deleted_task:
                self.db_connector.db.tasks.delete_one({'_id': task_id})
                return deleted_task
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the task data: {e}')
            return jsonify({'error': f'Error deleting the task data: {e}'}), 500


