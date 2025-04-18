from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config["MONGO_URI"] = "mongodb://cinemaAdmin:SecurePassword123!@db:27017/cinema_db?authSource=cinema_db"
    
    # Инициализация расширений
    CORS(app)
    mongo.init_app(app)
    
    # Регистрация роутов
    from .backend.api import register_api_routes
    from .backend.routes import register_main_routes
    
    register_api_routes(app)
    register_main_routes(app)
    
    return app
