from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Создание индексов
        app.mongo.db.film.create_index([("title", "text")])
        app.mongo.db.person.create_index([("name", "text")])
        app.mongo.db.admin.create_index([("login", 1)], unique=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    