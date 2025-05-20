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


def add_film(title, year, directors, actors, description, country, duration, genres, budget, poster, video_path, ratings, type="film", episodes=[]):
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
        "video_path": video_path if type == "film" else None,
        "ratings": ratings,
        "type": type
    }

    # Если это сериал — добавляем массив серий
    if type == "series":
        payload["episodes"] = episodes

    response = requests.post(f"{API_URL}/api/films", json=payload)
    response.raise_for_status()
    film_id = response.json().get("id")
    print(f"{'Фильм' if type == 'film' else 'Сериал'} '{title}' успешно добавлен с ID: {film_id}")

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
    response.raise_for_status()
    print(f"Администратор {login} успешно зарегистрирован!")
    return login


if __name__ == "__main__":
    print("Добавляем режиссёров...")
    director_ids = {
        "Christopher Nolan": add_person("Christopher Nolan", "director"),
        "Wes Anderson": add_person("Wes Anderson", "director"),
        "Bong Joon-ho": add_person("Bong Joon-ho", "director"),
        "Denis Villeneuve": add_person("Denis Villeneuve", "director"),
        "Steven Spielberg": add_person("Steven Spielberg", "director"),
        "David Fincher": add_person("David Fincher", "director"),
        "Vince Gilligan": add_person("Vince Gilligan", "director"),
        "David Benioff": add_person("David Benioff", "director"),
        "Marta Kauffman": add_person("Marta Kauffman", "director"),
        "Matt Duffer": add_person("Matt Duffer", "director"),
        "Jon Favreau": add_person("Jon Favreau", "director"),
        "Lana Wachowski": add_person("Lana Wachowski", "director"),
        "Peter Jackson": add_person("Peter Jackson", "director"),
        "Robert Zemeckis": add_person("Robert Zemeckis", "director"),
        "Johan Renck": add_person("Johan Renck", "director"),
        "Peter Morgan": add_person("Peter Morgan", "director")
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
        "Bryan Cranston": add_person("Bryan Cranston", "actor"),
        "Aaron Paul": add_person("Aaron Paul", "actor"),
        "Peter Dinklage": add_person("Peter Dinklage", "actor"),
        "Jennifer Aniston": add_person("Jennifer Aniston", "actor"),
        "Courteney Cox": add_person("Courteney Cox", "actor"),
        "Matthew Perry": add_person("Matthew Perry", "actor"),
        "Millie Bobby Brown": add_person("Millie Bobby Brown", "actor"),
        "Gaten Matarazzo": add_person("Gaten Matarazzo", "actor"),
        "Pedro Pascal": add_person("Pedro Pascal", "actor"),
        "Matthew McConaughey": add_person("Matthew McConaughey", "actor"),
        "Keanu Reeves": add_person("Keanu Reeves", "actor"),
        "Henry Cavill": add_person("Henry Cavill", "actor"),
        "Jared Harris": add_person("Jared Harris", "actor"),
        "Stellan Skarsgård": add_person("Stellan Skarsgård", "actor"),
        "Claire Foy": add_person("Claire Foy", "actor"),
        "Matt Smith": add_person("Matt Smith", "actor"),
        "Elijah Wood": add_person("Elijah Wood", "actor"),
        "Viggo Mortensen": add_person("Viggo Mortensen", "actor")
    }

    print("Добавляем фильмы...")

    add_film(
        title="Inception",
        year=2010,
        directors=[director_ids["Christopher Nolan"]],
        actors=[actor_ids["Leonardo DiCaprio"]],
        description="A thief who steals corporate secrets through dream-sharing technology",
        country="США",
        duration=148,
        genres=["Фантастика", "Боевик"],
        budget=160000000,
        poster="https://i.pinimg.com/736x/6f/c5/a3/6fc5a3240f09d882606e55da4a58b2dd.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
        type="film"
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
        type="film"
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
        type="film"
    )

    add_film(
        title="Dune",
        year=2021,
        directors=[director_ids["Denis Villeneuve"]],
        actors=[actor_ids["Timothée Chalamet"]],
        description="Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and vital element in the galaxy.",
        country="США",
        duration=155,
        genres=["Фантастика", "Приключения"],
        budget=165000000,
        poster="https://static.kinoafisha.info/k/movie_posters/1920x1080/upload/movie_posters/4/0/2/8355204/9ff0dfea8286428827af7478fdcd86a7.jpeg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
        type="film"
    )

    add_film(
        title="Saving Private Ryan",
        year=1998,
        directors=[director_ids["Steven Spielberg"]],
        actors=[actor_ids["Tom Hanks"]],
        description="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        country="США",
        duration=169,
        genres=["Военный", "Драма"],
        budget=70000000,
        poster="https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
        type="film"
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
        type="film"
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
        type="film"
    )
    
    add_film(
        title="Interstellar",
        year=2014,
        directors=[director_ids["Christopher Nolan"]],
        actors=[actor_ids["Matthew McConaughey"]],
        description="A team of explorers travel through a wormhole in space to ensure humanity's survival.",
        country="США",
        duration=169,
        genres=["Фантастика", "Приключения"],
        budget=165000000,
        poster="https://i.pinimg.com/474x/8e/0d/ab/8e0dab8699be85720ce55845065bf6dc.jpg?nii=t",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[8],
        type="film"
    )

    add_film(
        title="The Matrix",
        year=1999,
        directors=[director_ids["Lana Wachowski"]],
        actors=[actor_ids["Keanu Reeves"]],
        description="A computer programmer discovers a mysterious world of digital reality.",
        country="США",
        duration=136,
        genres=["Фантастика", "Боевик"],
        budget=63000000,
        poster="https://i.pinimg.com/originals/9e/85/34/9e8534c48e0168fb753057370627db8a.jpg",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
        type="film"
    )

    add_film(
        title="Forrest Gump",
        year=1994,
        directors=[director_ids["Robert Zemeckis"]],
        actors=[actor_ids["Tom Hanks"]],
        description="The story of a man with low IQ who rose to greatness through sheer persistence.",
        country="США",
        duration=142,
        genres=["Драма", "Комедия"],
        budget=55000000,
        poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/3560b757-9b95-45ec-af8c-623972370f9d/1920x",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
        type="film"
    )

    add_film(
        title="The Lord of the Rings: The Fellowship of the Ring",
        year=2001,
        directors=[director_ids["Peter Jackson"]],
        actors=[actor_ids["Elijah Wood"], actor_ids["Viggo Mortensen"]],
        description="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
        country="США",
        duration=178,
        genres=["Фэнтези", "Приключения"],
        budget=93000000,
        poster="https://avatars.mds.yandex.net/i?id=3b4fdc2068d8e6018b1b7ce76be47b5b_l-4314299-images-thumbs&n=13",
        video_path=f"{ES_URL}/videos/sample.mp4",
        ratings=[9],
        type="film"
    )

    print("Добавляем сериалы...")

    breaking_bad_videos = [
        {"season": 1, "episode": 1, "title": "Пилот", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Кошелек или жизнь", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="Breaking Bad",
        year=2008,
        directors=[director_ids["Vince Gilligan"]],
        actors=[actor_ids["Bryan Cranston"], actor_ids["Aaron Paul"]],
        description="Учитель химии с диагнозом рак легких начинает производить метамфетамин, чтобы оставить деньги семье после своей смерти.",
        country="США",
        duration=47,
        genres=["Драма", "Криминал"],
        budget=3000000,
        poster="https://basket-12.wbbasket.ru/vol1841/part184133/184133381/images/big/1.webp",
        video_path=None,
        ratings=[9],
        type="series",
        episodes=breaking_bad_videos
    )

    game_of_thrones_videos = [
        {"season": 1, "episode": 1, "title": "Winter Is Coming", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "The Kingsroad", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="Game of Thrones",
        year=2011,
        directors=[director_ids["David Benioff"]],
        actors=[actor_ids["Peter Dinklage"]],
        description="Борьба за Железный трон между королевскими семьями после свержения династии Таргариенов.",
        country="США",
        duration=55,
        genres=["Фэнтези", "Драма"],
        budget=6000000,
        poster="https://avatars.mds.yandex.net/get-mpic/12261762/2a0000018c631a10350ff00e5bd6d035b41d/orig",
        video_path=None,
        ratings=[9],
        type="series",
        episodes=game_of_thrones_videos
    )

    friends_videos = [
        {"season": 1, "episode": 1, "title": "The One Where Monica Gets a Roommate", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "The One with the Sonogram at the Bar", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="Friends",
        year=1994,
        directors=[director_ids["Marta Kauffman"]],
        actors=[actor_ids["Jennifer Aniston"], actor_ids["Courteney Cox"], actor_ids["Matthew Perry"]],
        description="Шесть молодых людей из Нью-Йорка, на первый взгляд совершенно разных, но связанных дружбой, пытаются найти свое место в жизни и любви.",
        country="США",
        duration=22,
        genres=["Комедия", "Романтика"],
        budget=4000000,
        poster="https://avatars.mds.yandex.net/get-mpic/5278457/img_id4865946163684198142.jpeg/orig",
        video_path=None,
        ratings=[8],
        type="series",
        episodes=friends_videos
    )

    stranger_videos = [
        {"season": 1, "episode": 1, "title": "Chapter One: The Vanishing of Will Byers", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Chapter Two: The Weirdo on Maple Street", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="Stranger Things",
        year=2016,
        directors=[director_ids["Matt Duffer"]],
        actors=[actor_ids["Millie Bobby Brown"], actor_ids["Gaten Matarazzo"]],
        description="Группа детей сталкивается с параллельным миром и странными существами, когда их друг исчезает при загадочных обстоятельствах.",
        country="США",
        duration=50,
        genres=["Фантастика", "Триллер"],
        budget=8000000,
        poster="https://static.displate.com/1200x857/displate/2022-09-05/67f549944a390c766fd186979ddb0f97_76ae2aa56db908b08a17c67a7371903a.jpg",
        video_path=None,
        ratings=[8],
        type="series",
        episodes=stranger_videos
    )

    mandalorian_videos = [
        {"season": 1, "episode": 1, "title": "Chapter 1: The Mandalorian", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Chapter 2: The Child", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="The Mandalorian",
        year=2019,
        directors=[director_ids["Jon Favreau"]],
        actors=[actor_ids["Pedro Pascal"]],
        description="Заброшенный охотник за головами оказывается в центре галактической войны после того, как получает задание забрать ценного ребенка.",
        country="США",
        duration=30,
        genres=["Фантастика", "Приключения"],
        budget=15000000,
        poster="https://cdn.ananasposter.ru/image/cache/catalog/poster/pos23/31/71438-1000x830.jpg",
        video_path=None,
        ratings=[8],
        type="series",
        episodes=mandalorian_videos
    )
    
    # Сериал 1: The Witcher
    witcher_videos = [
        {"season": 1, "episode": 1, "title": "The End's Beginning", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Four Marks", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="The Witcher",
        year=2019,
        directors=[director_ids["Jon Favreau"]],
        actors=[actor_ids["Henry Cavill"]],
        description="A witcher is summoned to protect the kingdom from dark forces.",
        country="Poland",
        duration=55,
        genres=["Фэнтези", "Драма"],
        budget=7000000,
        poster="https://i.pinimg.com/736x/4e/e0/c0/4ee0c075b1c33fccc9c2b64e5771c29b.jpg",
        video_path=None,
        ratings=[8],
        type="series",
        episodes=witcher_videos
    )

    # Сериал 2: Chernobyl
    chernobyl_videos = [
        {"season": 1, "episode": 1, "title": "Взрыв", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Спасение", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="Chernobyl",
        year=2019,
        directors=[director_ids["Johan Renck"]],
        actors=[actor_ids["Jared Harris"], actor_ids["Stellan Skarsgård"]],
        description="Рассказ о катастрофе на Чернобыльской АЭС и ее последствиях для всего мира.",
        country="UK",
        duration=60,
        genres=["Исторический", "Драма"],
        budget=5000000,
        poster="https://mir-s3-cdn-cf.behance.net/project_modules/1400/a6f64381852991.5d0baa717de68.jpg",
        video_path=None,
        ratings=[9],
        type="series",
        episodes=chernobyl_videos
    )

    # Сериал 3: The Crown
    crown_videos = [
        {"season": 1, "episode": 1, "title": "Vergangenheit", "url": f"{ES_URL}/videos/sample.mp4"},
        {"season": 1, "episode": 2, "title": "Hyde Park Corner", "url": f"{ES_URL}/videos/sample.mp4"}
    ]
    add_film(
        title="The Crown",
        year=2016,
        directors=[director_ids["Peter Morgan"]],
        actors=[actor_ids["Claire Foy"], actor_ids["Matt Smith"]],
        description="Документальный сериал о жизни королевской семьи Великобритании.",
        country="UK",
        duration=60,
        genres=["Исторический", "Драма"],
        budget=13000000,
        poster="https://www.kino-teatr.ru/movie/poster/123479/85770.jpg",
        video_path=None,
        ratings=[9],
        type="series",
        episodes=crown_videos
    )

    print("Добавляем администратора...")
    add_admin("admin@admin.com", "123456")

    print("\nВсе тестовые данные успешно добавлены!")
    print("-----------------------------------")
