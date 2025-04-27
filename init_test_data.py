import requests

API_URL = "http://localhost:5000"

def add_person(name, role, birth_date, birth_place, wiki_link):
    payload = {
        "name": name,
        "role": role,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "wiki_link": wiki_link
    }
    response = requests.post(f"{API_URL}/api/persons", json=payload)
    response.raise_for_status()
    person_id = response.json().get("id")
    print(f"{role.capitalize()} добавлен с ID: {person_id}")
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
        "ratings": ratings,
    }
    response = requests.post(f"{API_URL}/api/films", json=payload)
    response.raise_for_status()
    print(f"Фильм '{title}' успешно добавлен!")

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
    nolan_id = add_person(
        name="Christopher Nolan",
        role="director",
        birth_date="1970-07-30",
        birth_place="London, England",
        wiki_link="https://en.wikipedia.org/wiki/Christopher_Nolan"
    )

    anderson_id = add_person(
        name="Wes Anderson",
        role="director",
        birth_date="1969-05-01",
        birth_place="Houston, Texas",
        wiki_link="https://en.wikipedia.org/wiki/Wes_Anderson"
    )

    bong_id = add_person(
        name="Bong Joon-ho",
        role="director",
        birth_date="1969-09-14",
        birth_place="Daegu, South Korea",
        wiki_link="https://en.wikipedia.org/wiki/Bong_Joon-ho"
    )

    villeneuve_id = add_person(
        name="Denis Villeneuve",
        role="director",
        birth_date="1967-10-03",
        birth_place="Gentilly, Quebec",
        wiki_link="https://en.wikipedia.org/wiki/Denis_Villeneuve"
    )

    spielberg_id = add_person(
        name="Steven Spielberg",
        role="director",
        birth_date="1946-12-18",
        birth_place="Cincinnati, Ohio",
        wiki_link="https://en.wikipedia.org/wiki/Steven_Spielberg"
    )

    print("Добавляем актёров...")
    leo_id = add_person(
        name="Leonardo DiCaprio",
        role="actor",
        birth_date="1974-11-11",
        birth_place="Los Angeles, USA",
        wiki_link="https://en.wikipedia.org/wiki/Leonardo_DiCaprio"
    )

    timothee_id = add_person(
        name="Timothée Chalamet",
        role="actor",
        birth_date="1995-12-27",
        birth_place="New York City, USA",
        wiki_link="https://en.wikipedia.org/wiki/Timoth%C3%A9e_Chalamet"
    )

    song_id = add_person(
        name="Song Kang-ho",
        role="actor",
        birth_date="1967-01-17",
        birth_place="Gimhae, South Korea",
        wiki_link="https://en.wikipedia.org/wiki/Song_Kang-ho"
    )

    ralph_id = add_person(
        name="Ralph Fiennes",
        role="actor",
        birth_date="1962-12-22",
        birth_place="Ipswich, England",
        wiki_link="https://en.wikipedia.org/wiki/Ralph_Fiennes"
    )

    tom_id = add_person(
        name="Tom Hanks",
        role="actor",
        birth_date="1956-07-09",
        birth_place="Concord, California",
        wiki_link="https://en.wikipedia.org/wiki/Tom_Hanks"
    )

    print("Добавляем фильмы...")
    add_film(
        title="Inception",
        year=2010,
        directors=[nolan_id],
        actors=[leo_id],
        description="A thief who steals corporate secrets through dream-sharing technology",
        country="USA",
        duration=148,
        genres=["sci-fi", "action"],
        budget=160000000,
        poster="https://i.pinimg.com/736x/6f/c5/a3/6fc5a3240f09d882606e55da4a58b2dd.jpg",
        video_path="/videos/inception.mp4",
        ratings=[7],
    )

    add_film(
        title="Parasite",
        year=2019,
        directors=[bong_id],
        actors=[song_id],
        description="Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        country="South Korea",
        duration=132,
        genres=["drama", "thriller"],
        budget=11400000,
        poster="https://i.pinimg.com/736x/f3/17/a6/f317a612d86d1e324e4bd507cbf160aa.jpg",
        video_path="/videos/parasite.mp4",
        ratings=[7],
    )

    add_film(
        title="The Grand Budapest Hotel",
        year=2014,
        directors=[anderson_id],
        actors=[ralph_id],
        description="A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy.",
        country="Germany",
        duration=99,
        genres=["comedy", "drama"],
        budget=25000000,
        poster="https://cdn.ananasposter.ru/image/cache/catalog/poster/pos23/23/68397-1000x830.jpg",
        video_path="/videos/grand_budapest.mp4",
        ratings=[8],
    )

    add_film(
        title="Dune",
        year=2021,
        directors=[villeneuve_id],
        actors=[timothee_id],
        description="Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and vital element in the galaxy.",
        country="USA",
        duration=155,
        genres=["sci-fi", "adventure"],
        budget=165000000,
        poster="https://static.kinoafisha.info/k/movie_posters/1920x1080/upload/movie_posters/4/0/2/8355204/9ff0dfea8286428827af7478fdcd86a7.jpeg",
        video_path="/videos/dune.mp4",
        ratings=[8],
    )

    add_film(
        title="Saving Private Ryan",
        year=1998,
        directors=[spielberg_id],
        actors=[tom_id],
        description="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        country="USA",
        duration=169,
        genres=["war", "drama"],
        budget=70000000,
        poster="https://posterspy.com/wp-content/uploads/2019/10/Saving_private_ryan_poster_NEW.jpg",
        video_path="/videos/saving_ryan.mp4",
        ratings=[8],
    )

    print("Добавляем администратора...")
    admin_id = add_admin(
        login="admin123@mail.ru",
        password="123456"
    )

    print("\nТестовые данные успешно добавлены!")
    print("-----------------------------------")
