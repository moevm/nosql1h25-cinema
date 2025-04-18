from flask import render_template, jsonify, redirect, url_for
import os

def register_main_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/admin')
    def admin():
        return render_template('login.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return redirect(url_for('home'))
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405
