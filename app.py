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

db_connector = BookModel()
db_connector.connect_to_database()

book_service = BookService(db_connector)
book_schema = BookSchema()

book_blueprint = BookRoutes(book_service, book_schema)
app.register_blueprint(book_blueprint)

CORS(app, resources={r'/api/books': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.close_connection()