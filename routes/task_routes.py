from flask import jsonify, Blueprint, request
from marshmallow import ValidationError
from logger.logger_base import log

class TaskRoutes(Blueprint):
    def __init__(self, task_service, task_schema):
        super().__init__('task', __name__)
        self.task_service = task_service
        self.task_schema = task_schema
        self.register_routes()

    def register_routes(self):
        self.route('/api/tasks', methods=['GET'])(self.get_tasks)
        self.route('/api/tasks/<int:task_id>', methods=['GET'])(self.get_tasks_by_id)
        self.route('/api/tasks', methods=['POST'])(self.add_task)
        self.route('/api/tasks/<int:task_id>', methods=['PUT'])(self.update_task)
        self.route('/api/tasks/<int:task_id>', methods=['DELETE'])(self.delete_task)

    def get_tasks(self):
        try:
            self.tasks = self.task_service.get_all_tasks()
            return jsonify(self.tasks), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_tasks_by_id(self, task_id):
        self.task = self.task_service.get_task_by_id(task_id)
        if self.task:
            return jsonify(self.task), 200
        else: 
            return jsonify({'error': 'Task not found'}), 404
        
    def add_task(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.name = self.data.get('name')
            self.description = self.data.get('description')
            self.date = self.data.get('date')
            self.status = self.data.get('status')

            try:
                self.task_schema.validate_name(self.name)
                self.task_schema.validate_description(self.description)
                self.task_schema.validate_date(self.date)
                self.task_schema.validate_status(self.status)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.new_task = {
                'name': self.name,
                'description': self.description,
                'date':self.date,
                'status':self.status
            }

            self.created_task = self.task_service.add_task(self.new_task)
            return jsonify(self.created_task), 201
        except Exception as e:
            log.critical(f'Error adding a new task to the database: {e}')

    def update_task(self, task_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.name = self.data.get('name')
            self.description = self.data.get('description')
            self.date = self.data.get('date')
            self.status = self.data.get('status')

            try:
                self.task_schema.validate_name(self.name)
                self.task_schema.validate_description(self.description)
                self.task_schema.validate_date(self.date)
                self.task_schema.validate_status(self.status)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.task_updated = self.task_service.update_task(task_id, self.data)

            if self.task_updated:
                return jsonify(self.task_updated), 200
            else:
                return jsonify({'error': 'Task not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the task in the database: {e}')

    def delete_task(self, task__id):
        try:
            self.task_updated = self.task_service.delete_task(task__id)
            if self.task_deleted:
                return jsonify(self.task_deleted), 200
            else:
                return jsonify({'error': 'Task not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the task in the database: {e}')
