from flask import render_template, jsonify
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
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.route('/admin/statistics', endpoint='statistics')
    def admin_statistics():
        return render_template('statistics.html')

    @app.route('/admin/editor', endpoint='editor')
    def editor():
        return render_template('editor.html')

    @app.route('/admin/backup', endpoint='backup')
    def backup():
        return render_template('backup.html')

    @app.route('/recommendations', endpoint='recommendations')
    def backup():
        return render_template('recommendations.html')

    @app.route('/movie/<string:movie_id>/persons')
    def movie_actors(movie_id):
        return render_template('persons.html')

    @app.route('/movie/<string:movie_id>')
    def movie_page(movie_id):
        print(f"Запрос фильма с ID: {movie_id}")
        return render_template('movie.html', movie_id=movie_id)
