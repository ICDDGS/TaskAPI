from flask import Flask
from models.task_models import TaskModel
from flask_swagger_ui import get_swaggerui_blueprint
from services.task_services import TaskServices
from routes.task_routes import TaskRoutes
from schemas.task_schemas import TaskSchema
from flask_cors import CORS

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db_connector = TaskModel()
db_connector.connect_to_database()

task_service = TaskServices(db_connector)
task_schema = TaskSchema()

task_blueprint = TaskRoutes(task_service, task_schema)
app.register_blueprint(task_blueprint)

CORS(app, resources={r'/api/tasks': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.close_connection()