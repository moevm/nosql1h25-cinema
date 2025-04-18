from flask import send_from_directory, jsonify
import os

def register_main_routes(app):
    @app.route('/')
    def home():
        return send_from_directory('../frontend/home/pages', 'home.html')
    
    @app.route('/home')
    def serve_home_page():
        return send_from_directory('../frontend/home/pages', 'index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405