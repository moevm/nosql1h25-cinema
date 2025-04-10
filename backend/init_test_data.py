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

def add_film(title, year, directors, actors, description, country, duration, genres, budget, poster, video_path):
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
        "video_path": video_path
    }
    response = requests.post(f"{API_URL}/api/films", json=payload)
    response.raise_for_status()
    print(f"Фильм '{title}' успешно добавлен!")

if __name__ == "__main__":
    print("Добавляем режиссера...")
    director_id = add_person(
        name="Christopher Nolan",
        role="director",
        birth_date="1970-07-30",
        birth_place="London, England",
        wiki_link="https://en.wikipedia.org/wiki/Christopher_Nolan"
    )

    print("Добавляем актера...")
    actor_id = add_person(
        name="Leonardo DiCaprio",
        role="actor",
        birth_date="1974-11-11",
        birth_place="Los Angeles, USA",
        wiki_link="https://en.wikipedia.org/wiki/Leonardo_DiCaprio"
    )

    print("Добавляем фильм...")
    add_film(
        title="Inception",
        year=2010,
        directors=[director_id],
        actors=[actor_id],
        description="A thief who steals corporate secrets through dream-sharing technology",
        country="USA",
        duration=148,
        genres=["sci-fi", "action"],
        budget=160000000,
        poster="inception.jpg",
        video_path="/videos/inception.mp4"
    )

    print("\nТестовые данные успешно добавлены!")
    print("-----------------------------------")
    print(f"Фильм: Inception (2010)")
    print(f"Режиссер: Christopher Nolan ({director_id})")
    print(f"Актер: Leonardo DiCaprio ({actor_id})")
