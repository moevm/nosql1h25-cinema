from .. import mongo
from flask import jsonify, request
from bson import json_util, ObjectId
import json
import bcrypt

from werkzeug.utils import secure_filename
from datetime import datetime
import os
UPLOAD_FOLDER_POSTERS = 'static/uploads/posters'
UPLOAD_FOLDER_VIDEOS = 'static/uploads/videos'
os.makedirs(UPLOAD_FOLDER_POSTERS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_VIDEOS, exist_ok=True)



def parse_json(data):
    return json.loads(json_util.dumps(data))

def register_api_routes(app):
    # ==================== РОУТЫ ДЛЯ ПЕРСОН ====================
    @app.route('/api/persons', methods=['GET', 'POST'])
    def handle_persons():
        if request.method == 'GET':
            persons = list(mongo.db.person.find())
            return parse_json(persons), 200

        if request.method == 'POST':
            data = request.get_json()
            required_fields = ['name', 'role', 'birth_date']

            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            try:
                person = {
                    "name": data['name'],
                    "role": data['role'],
                    "birth_date": datetime.fromisoformat(data['birth_date']),
                    "birth_place": data.get('birth_place', ''),
                    "wiki_link": data.get('wiki_link', ''),
                    "films_list": data.get('films_list', [])
                }

                result = mongo.db.person.insert_one(person)
                return jsonify({
                    "id": str(result.inserted_id),
                    "message": "Person created"
                }), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500


    @app.route('/api/persons/<string:person_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_person(person_id):
        if request.method == 'GET':
            person = mongo.db.person.find_one({"_id": ObjectId(person_id)})
            if not person:
                return jsonify({"error": "Person not found"}), 404
            return parse_json(person), 200

        if request.method == 'PUT':
            data = request.get_json()
            update_data = {k: v for k, v in data.items() if k != '_id'}

            if 'birth_date' in update_data:
                update_data['birth_date'] = datetime.fromisoformat(update_data['birth_date'])

            result = mongo.db.person.update_one(
                {"_id": ObjectId(person_id)},
                {"$set": update_data}
            )
            return jsonify({"modified_count": result.modified_count}), 200

        if request.method == 'DELETE':
            result = mongo.db.person.delete_one({"_id": ObjectId(person_id)})
            return jsonify({"deleted_count": result.deleted_count}), 200


    # ==================== РОУТЫ ДЛЯ ФИЛЬМОВ ====================
    @app.route('/api/content')
    def get_content():
        content_type = request.args.get('type', 'all')

        movies = list(mongo.db.film.find())

        if content_type == 'all':
            return jsonify(movies)
        elif content_type == 'films':
            return jsonify([m for m in movies if m['type'] == 'film'])
        elif content_type == 'series':
            return jsonify([m for m in movies if m['type'] == 'series'])

        return jsonify([])


    @app.route('/api/films', methods=['GET', 'POST'])
    def handle_films():
        if request.method == 'GET':
            films = list(mongo.db.film.find())
            return parse_json(films), 200

        if request.method == 'POST':
            data = request.get_json()
            required_fields = ['title', 'year', 'directors', 'actors']

            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            try:
                film = {
                    "title": data['title'],
                    "year": data['year'],
                    "directors": [ObjectId(d) for d in data['directors']],
                    "actors": [ObjectId(a) for a in data['actors']],
                    "description": data.get('description', ''),
                    "country": data.get('country', ''),
                    "duration": data.get('duration', 0),
                    "genres": data.get('genres', []),
                    "budget": data.get('budget'),
                    "poster": data.get('poster'),
                    "video_path": data.get('video_path'),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "ratings": [],
                    "views": []
                }

                result = mongo.db.film.insert_one(film)
                return jsonify({
                    "id": str(result.inserted_id),
                    "message": "Film created"
                }), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500

    @app.route('/api/films/upload', methods=['POST'])
    def upload_film():
        try:
            title = request.form.get('title')
            year = int(request.form.get('year'))
            description = request.form.get('description', '')
            country = request.form.get('country', '')
            duration = int(request.form.get('duration', 0))
            budget = float(request.form.get('budget', 0))
            genres = json.loads(request.form.get('genres', '[]'))

            # Получаем режиссёров и актёров как строки
            directors_raw = json.loads(request.form.get('directors', '[]'))
            actors_raw = json.loads(request.form.get('actors', '[]'))

            # Найти соответствующие ObjectId из коллекции person
            def get_person_ids_by_names(names, role):
                ids = []
                for name in names:
                    person = mongo.db.person.find_one({'name': name.strip()})
                    if person:
                        ids.append(person['_id'])
                    else:
                        new_person = {
                            "name": name.strip(),
                            "role": role,
                            "birth_date": datetime(1900, 1, 1),
                            "birth_place": "",
                            "wiki_link": "",
                            "films_list": []
                        }
                        result = mongo.db.person.insert_one(new_person)
                        ids.append(result.inserted_id)
                return ids

            # Используем роли
            director_ids = get_person_ids_by_names(directors_raw, "director")
            actor_ids = get_person_ids_by_names(actors_raw, "actor")


            # Загрузка файлов
            poster_file = request.files.get('poster')
            video_file = request.files.get('video')

            poster_path = ''
            if poster_file:
                filename = secure_filename(poster_file.filename)
                poster_path = os.path.join(UPLOAD_FOLDER_POSTERS, filename)
                poster_file.save(poster_path)

            video_path = ''
            if video_file:
                filename = secure_filename(video_file.filename)
                video_path = os.path.join(UPLOAD_FOLDER_VIDEOS, filename)
                video_file.save(video_path)

            film = {
                "title": title,
                "year": year,
                "description": description,
                "country": country,
                "duration": duration,
                "budget": budget,
                "genres": genres,
                "poster": poster_path,
                "video_path": video_path,
                "directors": director_ids,
                "actors": actor_ids,
                "ratings": [],
                "views": [],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

            result = mongo.db.film.insert_one(film)
            return jsonify({
                "id": str(result.inserted_id),
                "message": "Фильм успешно добавлен"
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ==================== УДАЛЕНИЕ ФИЛЬМА ====================
    @app.route('/api/films/<film_id>', methods=['DELETE', 'OPTIONS'])
    def delete_film(film_id):
        if request.method == 'OPTIONS':
            return '', 204  # Для preflight запроса

        try:
            result = mongo.db.film.delete_one({'_id': ObjectId(film_id)})

            if result.deleted_count == 0:
                return jsonify({"error": "Film not found"}), 404

            return jsonify({"message": "Film deleted"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # ==================== АДМИНИСТРИРОВАНИЕ ====================
    @app.route('/api/admin/register', methods=['POST'])
    def register_admin():
        data = request.get_json()
        if 'login' not in data or 'password' not in data:
            return jsonify({"error": "Missing login or password"}), 400

        if mongo.db.admin.find_one({"login": data['login']}):
            return jsonify({"error": "Admin already exists"}), 400

        hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        mongo.db.admin.insert_one({
            "login": data['login'],
            "password": hashed_pw.decode()
        })
        return jsonify({"message": "Admin registered"}), 201


    @app.route('/api/admin/login', methods=['POST'])
    def login_admin():
        data = request.get_json()
        admin = mongo.db.admin.find_one({"login": data['login']})

        if admin and bcrypt.checkpw(data['password'].encode(), admin['password'].encode()):
            return jsonify({"message": "Login successful"}), 200

        return jsonify({"error": "Invalid credentials"}), 401


    #фильтрация
    @app.route('/api/films/filter', methods=['POST'])
    def filter_films():
        try:
            filters = request.get_json()
            all_films = list(mongo.db.film.find())


            def match(film):
                if filters.get('genre') and filters['genre'] not in film.get('genres', []):
                    return False
                if filters.get('country') and filters['country'] != film.get('country'):
                    return False
                if filters.get('year'):
                    try:
                        if int(filters['year']) != film.get('year'):
                            return False
                    except ValueError:
                        return False
                if filters.get('director'):
                    director_name = filters['director'].strip().lower()
                    director_ids = film.get('directors', [])
                    found = False
                    for d_id in director_ids:
                        person = mongo.db.person.find_one({"_id": d_id})
                        if person and director_name in person['name'].lower():
                            found = True
                            break
                    if not found:
                        return False
                if filters.get('actor'):
                    actor_name = filters['actor'].strip().lower()
                    actor_ids = film.get('actors', [])
                    found = False
                    for a_id in actor_ids:
                        person = mongo.db.person.find_one({"_id": a_id})
                        if person and actor_name in person['name'].lower():
                            found = True
                            break
                    if not found:
                        return False
                if filters.get('rating'):
                    try:
                        target_rating = float(filters['rating'])
                        ratings = film.get('ratings', [])
                        avg_rating = sum(ratings) / len(ratings) if ratings else 0
                        if avg_rating < target_rating:
                            return False
                    except:
                        return False
                if filters.get('added'):
                    try:
                        if str(film.get('created_at', ''))[:10] != filters['added']:
                            return False
                    except:
                        return False
                if filters.get('edited'):
                    try:
                        if str(film.get('updated_at', ''))[:10] != filters['edited']:
                            return False
                    except:
                        return False

                return True

            filtered = [film for film in all_films if match(film)]

            for film in filtered:
                film['_id'] = str(film['_id'])
                if 'created_at' in film:
                    film['created_at'] = str(film['created_at'])
                if 'updated_at' in film:
                    film['updated_at'] = str(film['updated_at'])

            return jsonify(filtered), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/films/search', methods=['POST'])
    def search_films():
        try:
            query = request.get_json()

            search_title = query.get('title', '').strip().lower()

            if not search_title:
                return jsonify([]), 200

            all_films = mongo.db.film.find({"title": {"$regex": search_title, "$options": "i"}})

            filtered_films = list(all_films)

            for film in filtered_films:
                film['_id'] = str(film['_id'])
                if 'created_at' in film:
                    film['created_at'] = str(film['created_at'])
                if 'updated_at' in film:
                    film['updated_at'] = str(film['updated_at'])

            return jsonify(filtered_films), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500






