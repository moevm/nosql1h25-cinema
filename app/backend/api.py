from app.backend.wiki_api import fetch_wikidata_person_info

from bson.errors import InvalidId

from .. import mongo
from flask import jsonify, request, send_from_directory, Response
from bson import json_util, ObjectId
import json
import bcrypt
from datetime import datetime


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
            required_fields = ['name', 'role']

            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            try:
                # Пытаемся получить данные из Wikidata
                wikidata_info = fetch_wikidata_person_info(data['name'])
                
                # Формируем объект персоны
                person = {
                    "name": data['name'],
                    "role": data['role'],
                    "birth_date": datetime.fromisoformat(data['birth_date']) if data.get('birth_date') else (
                        datetime.fromisoformat(wikidata_info['birth_date']) if wikidata_info and wikidata_info.get('birth_date') else None
                    ),
                    "birth_place": data.get('birth_place') or (
                        wikidata_info['birth_place'] if wikidata_info and wikidata_info.get('birth_place') else ''
                    ),
                    "wiki_link": data.get('wiki_link') or (
                        wikidata_info['wiki_link'] if wikidata_info and wikidata_info.get('wiki_link') else ''
                    ),
                    "photo_url": wikidata_info['photo_url'] if wikidata_info and wikidata_info.get('photo_url') else None,
                    "films_list": data.get('films_list', []),
                    "data_source": "wikidata" if wikidata_info else "manual"
                }

                result = mongo.db.person.insert_one(person)
                return jsonify({
                    "id": str(result.inserted_id),
                    "message": "Person created",
                    "data_source": "wikidata" if wikidata_info else "manual"
                }), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500


    @app.route('/api/persons/<string:person_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
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

        if request.method == 'PATCH':
            data = request.get_json()
            film_id = data.get('add_film')

            if not film_id:
                return jsonify({"error": "Missing film ID"}), 400

            result = mongo.db.person.update_one(
                {"_id": ObjectId(person_id)},
                {"$addToSet": {"films_list": film_id}}  # Добавит, только если нет
            )
            return jsonify({"modified_count": result.modified_count}), 200


    @app.route('/api/<string:film_id>/persons', methods=['GET'])
    def get_actors_by_film(film_id):
        try:
            persons = list(mongo.db.person.find({"films_list": film_id}))

            actors = []
            directors = []

            for person in persons:
                person_data = {
                    "name": person.get("name"),
                    "birth_date": person.get("birth_date").isoformat() if person.get("birth_date") else None,
                    "birth_place": person.get("birth_place"),
                    "wiki_link": person.get("wiki_link"),
                    "photo_url": person.get("photo_url"),
                }
                role = person.get("role", "").lower()
                if role == "actor":
                    actors.append(person_data)
                elif role == "director":
                    directors.append(person_data)

            return jsonify({
                "actors": actors,
                "directors": directors
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route('/api/export')
    def export_db():
        try:
            # Собираем данные из всех коллекций
            database_data = {}

            # Получаем список всех коллекций в базе данных
            collections = mongo.db.list_collection_names()

            for collection_name in collections:
                # Получаем все документы из коллекции
                collection = mongo.db[collection_name]
                documents = list(collection.find())

                # Конвертируем ObjectId и другие специальные типы BSON
                serialized = json.loads(json_util.dumps(documents))
                database_data[collection_name] = serialized

            # Создаем JSON-ответ
            response = Response(
                json.dumps(database_data, indent=2, ensure_ascii=False),
                mimetype='application/json',
                headers={
                    'Content-Disposition': 'attachment; filename=full_database_export.json'
                }
            )

            return response

        except Exception as e:
            return json.dumps({'error': str(e)}), 500

    @app.route('/api/import', methods=['POST'])
    def import_db():
        try:
            # Проверяем наличие файла в запросе
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400

            uploaded_file = request.files['file']

            # Проверяем расширение файла
            if uploaded_file.filename.split('.')[-1].lower() != 'json':
                return jsonify({'error': 'Invalid file format'}), 400

            # Читаем и парсим JSON
            data = json.loads(uploaded_file.read().decode('utf-8'))

            # Конвертируем специальные типы данных из JSON в BSON
            converted_data = json_util.loads(json.dumps(data))

            total_imported = 0  # <-- добавим счётчик

            # Очищаем существующие коллекции перед импортом
            for collection_name in converted_data.keys():
                mongo.db[collection_name].drop()

            # Импортируем данные
            for collection_name, documents in converted_data.items():
                collection = mongo.db[collection_name]
                if isinstance(documents, list):
                    result = collection.insert_many(documents)
                    total_imported += len(result.inserted_ids)
                else:
                    return jsonify({'error': f'Invalid format for collection {collection_name}'}), 400

            return jsonify({
                'message': 'Database imported successfully',
                'collections': list(converted_data.keys()),
                'importedCount': total_imported  # <-- добавляем в ответ
            }), 200

        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON file'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    # ==================== РОУТЫ ДЛЯ ФИЛЬМОВ ====================
    @app.route('/api/content')
    def get_content():
        try:
            content_type = request.args.get('type', 'all')
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 15))
            
            query = {}
            if content_type == 'films':
                query['type'] = 'film'
            elif content_type == 'series':
                query['type'] = 'series'

            
            all_films = list(mongo.db.film.find(query))
            
            total_items = len(all_films)
            start = (page - 1) * limit
            end = start + limit
            paginated_films = all_films[start:end]
            
            return parse_json({
                "films": paginated_films,
                "count": total_items
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/api/films', methods=['GET', 'POST'])
    def handle_films():
        if request.method == 'GET':
            try:
                films = mongo.db.film.find()
                    
                return parse_json(films), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        if request.method == 'POST':
            data = request.get_json()
            required_fields = ['title', 'year', 'directors', 'actors']

            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            try:
                # Определяем тип контента: фильм или сериал
                content_type = data.get('type', 'film')  # По умолчанию film
                
                # Базовые поля
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
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "ratings": data.get('ratings', []),
                    "views": [],
                    "type": content_type
                }

                # Поля, зависящие от типа
                if content_type == 'series':
                    episodes = data.get('episodes', [])
                    # Проверка формата видео-сериалов
                    for v in episodes:
                        if not all(k in v for k in ('season', 'episode', 'title', 'url')):
                            return jsonify({"error": "Invalid video format for series"}), 400
                    film["episodes"] = episodes
                    film["video_path"] = None  # Не используется для сериалов
                else:
                    film["video_path"] = data.get('video_path')
                    film["episodes"] = []  # Не используется для фильмов

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
            type = request.form.get('type', 'movie')

            directors_raw = json.loads(request.form.get('directors', '[]'))
            actors_raw = json.loads(request.form.get('actors', '[]'))

            # Найти соответствующие ObjectId из коллекции person
            def get_person_ids_by_names(names, role):
                ids = []
                for name in names:
                    # Сначала проверяем, есть ли такой человек в базе
                    person = mongo.db.person.find_one({'name': name.strip()})
                    if person:
                        ids.append(person['_id'])
                    else:
                        # Если нет, пробуем получить данные из Wikidata
                        wikidata_info = fetch_wikidata_person_info(name.strip())
                        
                        new_person = {
                            "name": name.strip(),
                            "role": role,
                            "birth_date": (
                                datetime.fromisoformat(wikidata_info['birth_date']) 
                                if wikidata_info and wikidata_info.get('birth_date') 
                                else datetime(1900, 1, 1)
                            ),
                            "birth_place": (
                                wikidata_info['birth_place'] 
                                if wikidata_info and wikidata_info.get('birth_place') 
                                else ""
                            ),
                            "wiki_link": (
                                wikidata_info['wiki_link'] 
                                if wikidata_info and wikidata_info.get('wiki_link') 
                                else ""
                            ),
                            "photo_url": (
                                wikidata_info['photo_url'] 
                                if wikidata_info and wikidata_info.get('photo_url') 
                                else None
                            ),
                            "films_list": [],
                            "data_source": "wikidata" if wikidata_info else "manual"
                        }
                        
                        result = mongo.db.person.insert_one(new_person)
                        ids.append(result.inserted_id)
                return ids

            # Используем роли
            director_ids = get_person_ids_by_names(directors_raw, "director")
            actor_ids = get_person_ids_by_names(actors_raw, "actor")

            # Обработка серий для сериалов
            episodes = []
            if type == 'series':
                episodes_raw = request.form.get('episodes', '[]')
                try:
                    episodes = json.loads(episodes_raw)
                except json.JSONDecodeError:
                    episodes = []

            # Вместо загрузки файла, получаем ссылку на видео
            video_url = request.form.get('video_url', '')

            # Получаем ссылку на постер
            poster_url = request.form.get('poster_url', '') if type == 'movie' else None

            film = {
                "title": title,
                "year": year,
                "description": description,
                "country": country,
                "duration": duration,
                "budget": budget,
                "genres": genres,
                "poster": poster_url,
                "video_path": video_url,  # Сохраняем ссылку вместо пути к файлу
                "directors": director_ids,
                "actors": actor_ids,
                "ratings": [],
                "views": [],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "type": type,
                "episodes": episodes if type == 'series' else None
            }

            result = mongo.db.film.insert_one(film)
            film_id = result.inserted_id
            
            # Обновляем films_list для всех актеров и режиссеров
            all_person_ids = director_ids + actor_ids
            if all_person_ids:
                mongo.db.person.update_many(
                    {"_id": {"$in": all_person_ids}},
                    {"$addToSet": {"films_list": str(film_id)}}
                )

            return jsonify({
                "id": str(film_id),
                "message": "Фильм успешно добавлен",
                "type": type
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

    def safe_objectid(id_str):
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            return None

    @app.route('/api/films/<film_id>', methods=['PUT'])
    def update_film(film_id):
        try:
            film = mongo.db.film.find_one({"_id": ObjectId(film_id)})
            if not film:
                return jsonify({"error": "Фильм не найден"}), 404

            # Получаем текущих актеров и режиссеров как строки
            current_director_ids = [str(id) for id in film.get('directors', [])]
            current_actor_ids = [str(id) for id in film.get('actors', [])]
            all_current_person_ids = current_director_ids + current_actor_ids

            # Получаем обновленные данные фильма
            title = request.form.get('title', film['title'])
            year = int(request.form.get('year', film['year']))
            description = request.form.get('description', film['description'])
            country = request.form.get('country', film['country'])
            duration = int(request.form.get('duration', film['duration']))
            budget = float(request.form.get('budget', film['budget']))
            genres = json.loads(request.form.get('genres', json.dumps(film['genres'])))
            type = request.form.get('type', film.get('type', 'movie'))

            directors_raw = json.loads(request.form.get('directors', '[]'))
            actors_raw = json.loads(request.form.get('actors', '[]'))

            # Обработка серий для сериалов
            episodes = []
            if type == 'series':
                episodes_raw = request.form.get('episodes', '[]')
                try:
                    episodes = json.loads(episodes_raw)
                except json.JSONDecodeError:
                    episodes = film.get('episodes', [])

            def get_person_ids_by_names(names, role):
                ids = []
                for name in names:
                    person = mongo.db.person.find_one({'name': name.strip()})
                    if person:
                        ids.append(str(person['_id']))  # Сохраняем как строку
                    else:
                        wikidata_info = fetch_wikidata_person_info(name.strip())
                        
                        new_person = {
                            "name": name.strip(),
                            "role": role,
                            "birth_date": (
                                datetime.fromisoformat(wikidata_info['birth_date']) 
                                if wikidata_info and wikidata_info.get('birth_date') 
                                else datetime(1900, 1, 1)
                            ),
                            "birth_place": (
                                wikidata_info['birth_place'] 
                                if wikidata_info and wikidata_info.get('birth_place') 
                                else ""
                            ),
                            "wiki_link": (
                                wikidata_info['wiki_link'] 
                                if wikidata_info and wikidata_info.get('wiki_link') 
                                else ""
                            ),
                            "photo_url": (
                                wikidata_info['photo_url'] 
                                if wikidata_info and wikidata_info.get('photo_url') 
                                else None
                            ),
                            "films_list": [film_id],  # Добавляем текущий фильм сразу
                            "data_source": "wikidata" if wikidata_info else "manual"
                        }
                        
                        result = mongo.db.person.insert_one(new_person)
                        ids.append(str(result.inserted_id))  # Сохраняем как строку
                return ids

            director_ids = get_person_ids_by_names(directors_raw, "director")
            actor_ids = get_person_ids_by_names(actors_raw, "actor")
            all_new_person_ids = director_ids + actor_ids

            # Удаляем фильм из films_list у тех, кто больше не связан с фильмом
            removed_person_ids = list(set(all_current_person_ids) - set(all_new_person_ids))
            if removed_person_ids:
                mongo.db.person.update_many(
                    {"_id": {"$in": [ObjectId(id) for id in removed_person_ids]}},
                    {"$pull": {"films_list": film_id}}
                )

            # Добавляем фильм в films_list у новых связанных персон
            added_person_ids = list(set(all_new_person_ids) - set(all_current_person_ids))
            if added_person_ids:
                mongo.db.person.update_many(
                    {"_id": {"$in": [ObjectId(id) for id in added_person_ids]}},
                    {"$addToSet": {"films_list": film_id}}
                )

            # Получаем ссылку на видео и постер
            # video_url = request.form.get('video_url', film.get('video_path', ''))
            poster_url = request.form.get('poster_url', film.get('poster', ''))
            # Для фильмов получаем ссылку на видео, для сериалов - None
            video_url = request.form.get('video_url', film.get('video_path', '')) if type == 'movie' else None

            # Обновляем данные фильма
            updated_film = {
                "title": title,
                "year": year,
                "description": description,
                "country": country,
                "duration": duration,
                "budget": budget,
                "genres": genres,
                "poster": poster_url,
                "video_path": video_url,
                "directors": [ObjectId(id) for id in director_ids],  # Сохраняем как ObjectId
                "actors": [ObjectId(id) for id in actor_ids],       # Сохраняем как ObjectId
                "updated_at": datetime.now(),
                "type": type,
                "episodes": episodes if type == 'series' else None
            }

            mongo.db.film.update_one({"_id": ObjectId(film_id)}, {"$set": updated_film})
            return jsonify({"message": "Фильм успешно обновлён"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/movies/<movie_id>', methods=['GET'])
    def get_movie_by_id(movie_id):
        try:
            movie = mongo.db.film.find_one_or_404({"_id": ObjectId(movie_id)})

            directors = []
            for director_id in movie.get('directors', []):
                obj_id = safe_objectid(director_id)
                if obj_id:
                    person = mongo.db.person.find_one({"_id": obj_id})
                    if person:
                        directors.append({
                            "name": person['name'],
                            "birth_date": person.get('birth_date').isoformat() if person.get('birth_date') else None,
                            "birth_place": person.get('birth_place'),
                            "photo_url": person.get('photo_url'),
                            "wiki_link": person.get('wiki_link')
                        })

            actors = []
            for actor_id in movie.get('actors', []):
                obj_id = safe_objectid(actor_id)
                if obj_id:
                    person = mongo.db.person.find_one({"_id": obj_id})
                    if person:
                        actors.append({
                            "name": person['name'],
                            "birth_date": person.get('birth_date').isoformat() if person.get('birth_date') else None,
                            "birth_place": person.get('birth_place'),
                            "photo_url": person.get('photo_url'),
                            "wiki_link": person.get('wiki_link')
                        })

            movie_data = {
                "title": movie["title"],
                "year": movie["year"],
                "description": movie["description"],
                "country": movie["country"],
                "duration": movie["duration"],
                "budget": movie["budget"],
                "genres": movie["genres"],
                "directors": directors,
                "actors": actors,
                "poster": movie.get('poster'),
                "video": movie.get('video_path'),
                "created_at": movie.get("created_at").isoformat() if movie.get("created_at") else None,
                "updated_at": movie.get("updated_at").isoformat() if movie.get("updated_at") else None,
                "avg_rating": calculate_avg_rating(movie.get("ratings", [])),
                "type": movie.get("type", "movie"),
                "episodes": movie.get("episodes") if movie.get("type") == "series" else None
            }

            return jsonify(movie_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def calculate_avg_rating(ratings):
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)

    # ==================== ОБНОВЛЕНИЕ РЕЙТИНГА ФИЛЬМА ====================
    @app.route('/api/films/<film_id>/rate', methods=['POST'])
    def rate_film(film_id):
        try:
            data = request.get_json()
            if not data or 'rating' not in data:
                return jsonify({"error": "Отсутствует оценка"}), 400

            rating = int(data['rating'])
            if rating < 1 or rating > 10:
                return jsonify({"error": "Оценка должна быть от 1 до 10"}), 400

            # Проверяем существование фильма
            film = mongo.db.film.find_one({"_id": ObjectId(film_id)})
            if not film:
                return jsonify({"error": "Фильм не найден"}), 404

            # Просто добавляем новую оценку в массив ratings
            mongo.db.film.update_one(
                {"_id": ObjectId(film_id)},
                {"$push": {"ratings": rating}}
            )

            # Рассчитываем новый средний рейтинг
            updated_film = mongo.db.film.find_one({"_id": ObjectId(film_id)})
            avg_rating = calculate_avg_rating(updated_film.get('ratings', []))

            return jsonify({
                "success": True,
                "message": "Оценка сохранена",
                "newAvgRating": avg_rating
            }), 200

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
            page = int(filters.get('page', 1))
            limit = int(filters.get('limit', 15))

            def match(film):
                # Название серии
                if filters.get('seriesTitle'):
                    series_title = filters['seriesTitle'].strip().lower()
                    if film.get('type') != 'series':
                        return False
                    found = False
                    for episode in film.get('episodes', []):
                        if series_title in episode.get('title', '').lower():
                            found = True
                            break
                    if not found:
                        return False
                
                # Жанр
                if filters.get('genre') and filters['genre'] not in film.get('genres', []):
                    return False

                # Страна
                if filters.get('country') and filters['country'] != film.get('country'):
                    return False

                # Год (диапазон)
                try:
                    film_year = film.get('year')
                    year_min = int(filters.get('yearMin', 0)) if filters.get('yearMin') else None
                    year_max = int(filters.get('yearMax', 9999)) if filters.get('yearMax') else None
                    if (year_min and film_year < year_min) or (year_max and film_year > year_max):
                        return False
                except:
                    return False

                # Режиссёр
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

                # Актёр
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

                # Рейтинг (диапазон)
                try:
                    ratings = film.get('ratings', [])
                    avg_rating = sum(ratings) / len(ratings) if ratings else 1
                    rating_min = float(filters.get('ratingMin', 1))
                    rating_max = float(filters.get('ratingMax', 10))
                    if avg_rating < rating_min or avg_rating > rating_max:
                        return False
                except:
                    return False

                # Дата добавления (от - до)
                try:
                    added_date = str(film.get('created_at', ''))[:10]
                    if filters.get('addedMin') and added_date < filters['addedMin']:
                        return False
                    if filters.get('addedMax') and added_date > filters['addedMax']:
                        return False
                except:
                    return False

                # Дата редактирования (от - до)
                try:
                    edited_date = str(film.get('updated_at', ''))[:10]
                    if filters.get('editedMin') and edited_date < filters['editedMin']:
                        return False
                    if filters.get('editedMax') and edited_date > filters['editedMax']:
                        return False
                except:
                    return False

                # Описание (поиск подстроки)
                if filters.get('description'):
                    desc = film.get('description', '')
                    if not isinstance(desc, str) or filters['description'].strip().lower() not in desc.lower():
                        return False

                # Длительность (в минутах, диапазон)
                try:
                    duration = film.get('duration')
                    duration_min = int(filters['durationMin']) if filters.get('durationMin') else None
                    duration_max = int(filters['durationMax']) if filters.get('durationMax') else None
                    if duration is not None:
                        if duration_min is not None and duration < duration_min:
                            return False
                        if duration_max is not None and duration > duration_max:
                            return False
                    elif duration_min is not None or duration_max is not None:
                        return False
                except:
                    return False

                # Бюджет (в миллионах, диапазон)
                try:
                    budget = film.get('budget')
                    budget_min = int(filters['budgetMin']) if filters.get('budgetMin') else None
                    budget_max = int(filters.get('budgetMax')) if filters.get('budgetMax') else None
                    if budget is not None:
                        if budget_min is not None and budget < budget_min:
                            return False
                        if budget_max is not None and budget > budget_max:
                            return False
                    elif budget_min is not None or budget_max is not None:
                        return False
                except:
                    return False

                return True

            all_films = list(mongo.db.film.find())
            filtered = [film for film in all_films if match(film)]
            
            total_items = len(filtered)
            start = (page - 1) * limit
            end = start + limit
            paginated_films = filtered[start:end]

            for film in paginated_films:
                film['_id'] = str(film['_id'])
                if 'created_at' in film:
                    film['created_at'] = str(film['created_at'])
                if 'updated_at' in film:
                    film['updated_at'] = str(film['updated_at'])

            return jsonify({
                "films": paginated_films,
                "count": total_items
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @app.route('/api/films/search', methods=['POST'])
    def search_films():
        try:
            query = request.get_json()
            search_title = query.get('title', '').strip().lower()
            if not search_title:
                return jsonify({"films": [], "count": 0}), 200

            all_films = mongo.db.film.find({"title": {"$regex": search_title, "$options": "i"}})
            filtered_films = list(all_films)

            # Пагинация
            page = int(query.get('page', 1))
            limit = int(query.get('limit', 15))
            start = (page - 1) * limit
            end = start + limit
            paginated_films = filtered_films[start:end]

            for film in paginated_films:
                film['_id'] = str(film['_id'])
                if 'created_at' in film:
                    film['created_at'] = str(film['created_at'])
                if 'updated_at' in film:
                    film['updated_at'] = str(film['updated_at'])

            return jsonify({
                "films": paginated_films,
                "count": len(filtered_films)
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
