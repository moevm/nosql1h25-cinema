import requests

API_URL = "http://localhost:5000"
ES_URL = "http://92.100.72.29"


def add_person(name, role):
    payload = {
        "name": name,
        "role": role
    }
    response = requests.post(f"{API_URL}/api/persons", json=payload)
    response.raise_for_status()
    person_id = response.json().get("id")
    print(f"{role.capitalize()} '{name}' добавлен с ID: {person_id}")
    return person_id

def add_film(title, year, directors, actors, description, country, duration, genres, budget, poster, video_path, ratings):
    payload = {
        "title": title,
        "year": year,
        "directors": directors,
        "actors": actors,
        "description": description,
        "country": country,
        "duration": duration,
        "genres": genres,
        "budget": budget,
        "poster": poster,
        "video_path": video_path,
        "ratings": ratings
    }
    response = requests.post(f"{API_URL}/api/films", json=payload)
    response.raise_for_status()

    film_id = response.json().get("id")
    print(f"Фильм '{title}' успешно добавлен с ID: {film_id}")

    # Обновляем фильмографии режиссёров и актёров
    for person_id in directors + actors:
        update_person_films(person_id, film_id)

    return film_id

def update_person_films(person_id, film_id):
    payload = {"add_film": film_id}
    response = requests.patch(f"{API_URL}/api/persons/{person_id}", json=payload)
    response.raise_for_status()
    print(f"Фильм {film_id} добавлен в фильмографию персоны {person_id}")

def add_admin(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f"{API_URL}/api/admin/register", json=payload)
    response.raise_for_status()  # Проверка на успешность запроса
    print(f"Администратор {login} успешно зарегистрирован!")
    return login  # Можно вернуть login, или ID, если он возвращается в ответе



if __name__ == "__main__":
    print("Добавляем режиссёров...")
    director_ids = {
        "Christopher Nolan": add_person("Christopher Nolan", "director"),
        "Wes Anderson": add_person("Wes Anderson", "director"),
        "Bong Joon-ho": add_person("Bong Joon-ho", "director"),
        "Denis Villeneuve": add_person("Denis Villeneuve", "director"),
        "Steven Spielberg": add_person("Steven Spielberg", "director"),
        "David Fincher": add_person("David Fincher", "director"),
    }

    print("Добавляем актёров...")
    actor_ids = {
        "Leonardo DiCaprio": add_person("Leonardo DiCaprio", "actor"),
        "Timothée Chalamet": add_person("Timothée Chalamet", "actor"),
        "Song Kang-ho": add_person("Song Kang-ho", "actor"),
        "Ralph Fiennes": add_person("Ralph Fiennes", "actor"),
        "Tom Hanks": add_person("Tom Hanks", "actor"),
        "Brad Pitt": add_person("Brad Pitt", "actor"),
        "Edward Norton": add_person("Edward Norton", "actor"),
        "Christian Bale": add_person("Christian Bale", "actor"),
        "Heath Ledger": add_person("Heath Ledger", "actor"),
    }


    print("Добавляем фильмы...")
    add_film(
        title="Inception",
        year=2010,
        directors=[director_ids["Christopher Nolan"]],
        actors=[actor_ids["Leonardo DiCaprio"]],
        description="A thief who steals corporate secrets through dream-sharing technology",
        country="USA",
        duration=148,
        genres=["Фантастика", "Боевик"],
        budget=160000000,
        poster="https://i.pinimg.com/736x/6f/c5/a3/6fc5a3240f09d882606e55da4a58b2dd.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
    )

    add_film(
        title="Parasite",
        year=2019,
        directors=[director_ids["Bong Joon-ho"]],
        actors=[actor_ids["Song Kang-ho"]],
        description="Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        country="South Korea",
        duration=132,
        genres=["Драма", "Триллер"],
        budget=11400000,
        poster="https://i.pinimg.com/736x/f3/17/a6/f317a612d86d1e324e4bd507cbf160aa.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[7],
    )

    add_film(
        title="The Grand Budapest Hotel",
        year=2014,
        directors=[director_ids["Wes Anderson"]],
        actors=[actor_ids["Ralph Fiennes"]],
        description="A writer encounters the owner of an aging high-class hotel, who tells him of his early years as a lobby boy.",
        country="Germany",
        duration=99,
        genres=["Комедия", "Драма"],
        budget=25000000,
        poster="https://cdn.ananasposter.ru/image/cache/catalog/poster/pos23/23/68397-1000x830.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
    )

    add_film(
        title="Dune",
        year=2021,
        directors=[director_ids["Denis Villeneuve"]],
        actors=[actor_ids["Timothée Chalamet"]],
        description="Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and vital element in the galaxy.",
        country="USA",
        duration=155,
        genres=["Фантастика", "Приключения"],
        budget=165000000,
        poster="https://static.kinoafisha.info/k/movie_posters/1920x1080/upload/movie_posters/4/0/2/8355204/9ff0dfea8286428827af7478fdcd86a7.jpeg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
    )

    add_film(
        title="Saving Private Ryan",
        year=1998,
        directors=[director_ids["Steven Spielberg"]],
        actors=[actor_ids["Tom Hanks"]],
        description="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        country="USA",
        duration=169,
        genres=["Военный", "Драма"],
        budget=70000000,
        poster="https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
    )

    add_film(
        title="Бойцовский клуб",
        year=1999,
        directors=[director_ids["David Fincher"]],
        actors=[actor_ids["Brad Pitt"], actor_ids["Edward Norton"]],
        description="Офисный работник встречает продавца мыла, и они создают бойцовский клуб.",
        country="США",
        duration=139,
        genres=["Драма", "Триллер"],
        budget=63000000,
        poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1777765/6c5cdb4c-5e28-4552-aac4-beb4efaf718d/3840x",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
    )

    add_film(
        title="Темный рыцарь",
        year=2008,
        directors=[director_ids["Christopher Nolan"]],
        actors=[actor_ids["Christian Bale"], actor_ids["Heath Ledger"]],
        description="Бэтмен сталкивается с новым преступником по прозвищу Джокер, который бросает вызов всей системе правосудия в Готэме.",
        country="США",
        duration=152,
        genres=["Боевик", "Криминал", "Драма"],
        budget=185000000,
        poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/0fa5bf50-d5ad-446f-a599-b26d070c8b99/600x900",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
    )

    print("Добавляем администратора...")
    add_admin("admin@admin.com", "123456")

    print("\nВсе тестовые данные успешно добавлены!")
    print("-----------------------------------")
