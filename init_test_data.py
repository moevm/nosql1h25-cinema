import requests

API_URL = "http://localhost:5000"

def add_person(name, role, birth_date, birth_place, wiki_link, film_ids=None):
    payload = {
        "name": name,
        "role": role,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "wiki_link": wiki_link,
        "films": film_ids
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

    fincher_id = add_person(
        name="David Fincher",
        role="director",
        birth_date="1962-08-28",
        birth_place="Denver, Colorado",
        wiki_link="https://en.wikipedia.org/wiki/David_Fincher"
    )

    jeunet_id = add_person(
        name="Jean-Pierre Jeunet",
        role="director",
        birth_date="1953-09-03",
        birth_place="Roanne, France",
        wiki_link="https://en.wikipedia.org/wiki/Jean-Pierre_Jeunet"
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

    pitt_id = add_person(
        name="Brad Pitt",
        role="actor",
        birth_date="1963-12-18",
        birth_place="Shawnee, Oklahoma",
        wiki_link="https://en.wikipedia.org/wiki/Brad_Pitt"
    )

    norton_id = add_person(
        name="Edward Norton",
        role="actor",
        birth_date="1969-08-18",
        birth_place="Boston, Massachusetts",
        wiki_link="https://en.wikipedia.org/wiki/Edward_Norton"
    )

    bale_id = add_person(
        name="Christian Bale",
        role="actor",
        birth_date="1974-01-30",
        birth_place="Haverfordwest, Wales",
        wiki_link="https://en.wikipedia.org/wiki/Christian_Bale"
    )

    ledger_id = add_person(
        name="Heath Ledger",
        role="actor",
        birth_date="1979-04-04",
        birth_place="Perth, Western Australia",
        wiki_link="https://en.wikipedia.org/wiki/Heath_Ledger"
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
        genres=["Фантастика", "Боевик"],
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
        genres=["Драма", "Триллер"],
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
        genres=["Комедия", "Драма"],
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
        genres=["Фантастика", "Приключения"],
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
        genres=["Военный", "Драма"],
        budget=70000000,
        poster="https://kinopoisk-ru.clstorage.net/2k9Q8j399/dc680cQXLs9/wwoOejflX9IqEwH6amZHAdAhLCeTmyPjWC_EKiicd0opJZEUZfijOFNG8dJjjM6cDbApmBEpYIyBS0zsws-oLUIaT23zdgkGvZRTrv1zEpNWI7m01Yk2cF55AGZkkDzA4iyO3G9yqXzFV3eEtNkYTZ2mLM4WebEXT4gar4_FPvzPQQUytrWUHWpKAT4gLAeOCuznKwjcqSXP64rlr9OyxuYvz9PldC4_BVlihbWYWcqfLuIISfswEEqVEmsGDjK5AQPCOnOw3h5tRoz2rO3PhQ6gK-7CX6cuzmeMJ-EZ_wmvo4wd5LEntMBfJoV0GBIA1KDmCcHx95QAG9EvgAQ3tQkMhPy5_lBVZM1C-OMszg0ILuUnQ5yj446sxeEpUbrKLWUJWmd7ID3NW2VEt1PbAV6posBIt3hZg1Ud7AMMcbVPCQx3cffa2a3LAT-tpQpCB27hqIDZrquHK0aiLRF2jairyVyieG51xV-qjbgR0IVcKmwBTD72mc4dWeZLTXJxBckGdPl9Hp1vyUNz5GsNyYGgbysDUKioTy_EIK8e_Egnpc4T4jqnckkWYoS0kloM2uQjDwj-dxUA3l5rSMQwcMbNjvUzdl4Vq8kNdGusjQ6Kbq9sjBvjo0cjRyAt3HKEZyZG1G71p7pA1uDLvlYSTJepYUmJ-33ehlCTZwIMvT3KQ8z9sn4ZXysIDbAs6cqLSi6sIgjaaeRArUQlr5A0wuQtSFTtPmA3SphkjPQU2stepSqNQ_c4UYGVnqcOQfC1B80NuLA2XR9mDgo5YGYCgktmqGMNk25gzWbI6ykd9UpgroRfKzVk8MTYZMB139UIVCysiAgwcBjKWdYvRgW3-IIDTXIytZxQpkIMs6MqBsdAJODnBBZsp0FnS6kg1H2J4GHPHeIyoHGBFOyD_VveyBTmpM3OsfQQSRKQo8_D8_JKRQs7NjXUUSsBSjcorA0HAunsbMFWrmaK7Y3r6JJ8QyanAJRneup7yxokTPiQGoFX7y4GwbQ4XUFZnm8Iyru9zQ0NdLL70tYrRs9-ZO4GC0hnq-IEFizigCWDYO1WfkDupooerjlpvMRU6AL6XpgJ1KWpzskxMtqFFpFhAUfx_MoPRPV5_NaYq0YLtqhvy06GqytmSJcv7EBpw-CoGvFCq2KG3OtwL3pFniFDfJMfghan6wBGffzYSRqTL0cOuDDPCUhz8HjQF63EAzFs6UMDD2ippIbfb-2I6w8to5Y_ia-mQp6sdCS0ABgiT_zfXwwV7WyJw7jw2YgRUqlGRH10yAeEs3W1lhCizIK8Z22Cw4jgoSmDE6zsTuwP4SISuY2n4gBcqzxpv4MX6IW9nJfK32DiSExwvdsKXlYjS0P4sAMMCj2xOpnSI4qFtyttysvBKWnngBAkrMVuQiuiE3QLKe-OlGz8Y3HDF2INexLYgV4qIcUNf3iSTJmbLkKHuPMNAUw2cXSfkuoFz_MkbAWFCKSs7MHcouDIrAqkYNA3iuGjg96u-ib_A57sj38WV4pbKamOCLjx3UHWUKTOx7g9iMzFMLdzH1KjhAI6ZGWCR0kjqGHMki_jwG4D7aBW_01rboHVq_zu-AQf7k13XNGKECWigAh_PVLKmNOnyMq-Pk3OhDL1etwaaIsCfGWtRwnB5uQoSpGra4fugqBj0DRELy-C0GgzaTUL2W4GPhDdz9XsKU-Dez1RgVnbJoLLN_POz8r2-rzRECwFgjrrJotFDmZgoAvab2XG7w0jJxW8TKZviFvrseF7TBlugPzSEA-SbSOHAfY-3YAY0a_KTTbxScINs3G2HZBsBIZ8oGqFTsroLKuNX2Gsiy6M6uPQPsJgI08brXmgsYjfqEp3UJ4FXK0hhog5-lSFGx2nRwf--sqNSneyM93RZgYGM2vii4LHZOtqyhyubwusim3qED0MpS1AmCbwoXHNmyyFvB8YBRagaYSMPvIQBZQZKIMP-nMNT8Q4Nz_eVmOEC3rkLELLySZga8kc5iJNYUegKRV8QWdhBxoie6EzwdGhR_KRVwEWrapCjnl0EwCT1GeFwzh9DoEPePV0mdGvCUUx4uLGA0LhrqkDkOFiw-hAZakef8qrrEPa7X0qO8wRLUq7116B1O5kzAW9sNrA2tWjBYX79M4BQrR1e56bZAtGuaSpQgbDauHowxoh40usxCMmkX6Jr2MHFmv17nzOG2zOuxBeC5Ioo0DGM3zcihEZ5cYFOnRDCYX7c73RlaxLxPOjakLFga-vYAzWJOtALw3qJlS3junuS9OufCP5S1lgAvffmglTYKPMTD85G4pSGeEJhbD5i8pPcDY6XxUnSQTxra-DR4hk4W4GFmrtzi4FI2ra_M5rpkkW7bhsdwRXKcYw0ltInWJsRgN1t9JFm9ikiI05c48MDPRy-t6XbMqKNysnBQyJaWcpSJzgaA0oAqhlUP-JZykHk6R-r7iD2WSNP1-aR96mbg4BvfUaQ5mU6QgH8bMCxIQ0NjoZlWBKDTcvYwrHjmbuqkTf4KRHowWoYl7wTCwky1yveytxxpSpRTNT0UcUp2qHj3G2k41Q06jHhrF4jsxC_nV1WBarRM13ouNEyUPpKGgMmmGnQGiEJ-rd9cwlZYkfZ33mNUNbKMd7nNbF3-9iTcd88JmCXBGtyAW_8ojESLxwNdXW746M8S9miAqG4SBsApoo4gOhB-1pljUJ5acJVqc6ILOK3qVDPtMXT9xvLg0FtzCYylIRrcZK-TSPgQJ2Nb1XU6RFDDDrpg8PQuSrYMWWYy3G4IjqqpI0CuZrwt9iMi5wRtpuBTOTEUxVLuTATTtxEcqam-gOzP-7C4QP9Pm2GtaqQwozZWaMCkqnrySKliosRScO4qpSNEHvZosWYnzm8A1WYQ6wFpZCl20sR00zMBzLHZHoSIFzvEqPTDs6exQeZUqOP6mpQgwH7OtrwVdm5YmpS6_umb2JIeoPW644a_pDme3F8lvZSxpoYM8FO72Uhg",
        video_path="/videos/saving_ryan.mp4",
        ratings=[8],
    )

    add_film(
        title="Бойцовский клуб",
        year=1999,
        directors=[fincher_id],
        actors=[pitt_id, norton_id],
        description="Офисный работник страдает от бессонницы и встречает загадочного продавца мыла, с которым они основывают подпольный бойцовский клуб.",
        country="США",
        duration=139,
        genres=["Драма", "Триллер"],
        budget=63000000,
        poster="https://kinopoisk-ru.clstorage.net/2k9Q8j399/dc680cQXLs9/wwoOejflX9IqEwH6amZHAdAhLCeTmyPjWC_EKiicd0opJZEUZfijOFNHsRBiT46czbBo2RBooVkAC1k7Qs-oLUJP2u3lYtwTfZVSr-ixEAdWNztjwUk2cF55AGZkkDzA4iyO3G9yqXzFV3eEtNkYTZ2mLM4WebEXT4gar4_FPvzPQQUytrWUHWpKAT4gLAeOCuznKwjcqSXP64rlr9OyxuYvz9PldC4_BVlihbWYWcqfLuIISfswEEqVEmsGDjK5AQPCOnOw3h5tRoz2rO3PhQ6gK-7CX6cuzmeMJ-EZ_wmvo4wd5LEntMBfJoV0GBIA1KDmCcHx95QAG9EvgAQ3tQkMhPy5_lBVZM1C-OMszg0ILuUnQ5yj446sxeEpUbrKLWUJWmd7ID3NW2VEt1PbAV6posBIt3hZg1Ud7AMMcbVPCQx3cffa2a3LAT-tpQpCB27hqIDZrquHK0aiLRF2jairyVyieG51xV-qjbgR0IVcKmwBTD72mc4dWeZLTXJxBckGdPl9Hp1vyUNz5GsNyYGgbysDUKioTy_EIK8e_Egnpc4T4jqnckkWYoS0kloM2uQjDwj-dxUA3l5rSMQwcMbNjvUzdl4Vq8kNdGusjQ6Kbq9sjBvjo0cjRyAt3HKEZyZG1G71p7pA1uDLvlYSTJepYUmJ-33ehlCTZwIMvT3KQ8z9sn4ZXysIDbAs6cqLSi6sIgjaaeRArUQlr5A0wuQtSFTtPmA3SphkjPQU2stepSqNQ_c4UYGVnqcOQfC1B80NuLA2XR9mDgo5YGYCgktmqGMNk25gzWbI6ykd9UpgroRfKzVk8MTYZMB139UIVCysiAgwcBjKWdYvRgW3-IIDTXIytZxQpkIMs6MqBsdAJODnBBZsp0FnS6kg1H2J4GHPHeIyoHGBFOyD_VveyBTmpM3OsfQQSRKQo8_D8_JKRQs7NjXUUSsBSjcorA0HAunsbMFWrmaK7Y3r6JJ8QyanAJRneup7yxokTPiQGoFX7y4GwbQ4XUFZnm8Iyru9zQ0NdLL70tYrRs9-ZO4GC0hnq-IEFizigCWDYO1WfkDupooerjlpvMRU6AL6XpgJ1KWpzskxMtqFFpFhAUfx_MoPRPV5_NaYq0YLtqhvy06GqytmSJcv7EBpw-CoGvFCq2KG3OtwL3pFniFDfJMfghan6wBGffzYSRqTL0cOuDDPCUhz8HjQF63EAzFs6UMDD2ippIbfb-2I6w8to5Y_ia-mQp6sdCS0ABgiT_zfXwwV7WyJw7jw2YgRUqlGRH10yAeEs3W1lhCizIK8Z22Cw4jgoSmDE6zsTuwP4SISuY2n4gBcqzxpv4MX6IW9nJfK32DiSExwvdsKXlYjS0P4sAMMCj2xOpnSI4qFtyttysvBKWnngBAkrMVuQiuiE3QLKe-OlGz8Y3HDF2INexLYgV4qIcUNf3iSTJmbLkKHuPMNAUw2cXSfkuoFz_MkbAWFCKSs7MHcouDIrAqkYNA3iuGjg96u-ib_A57sj38WV4pbKamOCLjx3UHWUKTOx7g9iMzFMLdzH1KjhAI6ZGWCR0kjqGHMki_jwG4D7aBW_01rboHVq_zu-AQf7k13XNGKECWigAh_PVLKmNOnyMq-Pk3OhDL1etwaaIsCfGWtRwnB5uQoSpGra4fugqBj0DRELy-C0GgzaTUL2W4GPhDdz9XsKU-Dez1RgVnbJoLLN_POz8r2-rzRECwFgjrrJotFDmZgoAvab2XG7w0jJxW8TKZviFvrseF7TBlugPzSEA-SbSOHAfY-3YAY0a_KTTbxScINs3G2HZBsBIZ8oGqFTsroLKuNX2Gsiy6M6uPQPsJgI08brXmgsYjfqEp3UJ4FXK0hhog5-lSFGx2nRwf--sqNSneyM93RZgYGM2vii4LHZOtqyhyubwusim3qED0MpS1AmCbwoXHNmyyFvB8YBRagaYSMPvIQBZQZKIMP-nMNT8Q4Nz_eVmOEC3rkLELLySZga8kc5iJNYUegKRV8QWdhBxoie6EzwdGhR_KRVwEWrapCjnl0EwCT1GeFwzh9DoEPePV0mdGvCUUx4uLGA0LhrqkDkOFiw-hAZakef8qrrEPa7X0qO8wRLUq7116B1O5kzAW9sNrA2tWjBYX79M4BQrR1e56bZAtGuaSpQgbDauHowxoh40usxCMmkX6Jr2MHFmv17nzOG2zOuxBeC5Ioo0DGM3zcihEZ5cYFOnRDCYX7c73RlaxLxPOjakLFga-vYAzWJOtALw3qJlS3junuS9OufCP5S1lgAvffmglTYKPMTD85G4pSGeEJhbD5i8pPcDY6XxUnSQTxra-DR4hk4W4GFmrtzi4FI2ra_M5rpkkW7bhsdwRXKcYw0ltInWJsRgN1t9JFm9ikiI05c48MDPRy-t6XbMqKNysnBQyJaWcpSJzgaA0oAqhlUP-JZykHk6R-r7iD2WSNP1-aR96mbg4BvfUaQ5mU6QgH8bMCxIQ0NjoZlWBKDTcvYwrHjmbuqkTf4KRHowWoYl7wTCwky1yveytxxpSpRTNT0UcUp2qHj3G2k41Q06jHhrF4jsxC_nV1WBarRM13ouNEyUPpKGgMmmGnQGiEJ-rd9cwlZYkfZ33mNUNbKMd7nNbF3-9iTcd88JmCXBGtyAW_8ojESLxwNdXW746M8S9miAqG4SBsApoo4gOhB-1pljUJ5acJVqc6ILOK3qVDPtMXT9xvLg0FtzCYylIRrcZK-TSPgQJ2Nb1XU6RFDDDrpg8PQuSrYMWWYy3G4IjqqpI0CuZrwt9iMi5wRtpuBTOTEUxVLuTATTtxEcqam-gOzP-7C4QP9Pm2GtaqQwozZWaMCkqnrySKliosRScO4qpSNEHvZosWYnzm8A1WYQ6wFpZCl20sR00zMBzLHZHoSIFzvEqPTDs6exQeZUqOP6mpQgwH7OtrwVdm5YmpS6_umb2JIeoPW644a_pDme3F8lvZSxpoYM8FO72Uhg",
        video_path="/videos/fight_club.mp4",
        ratings=[9],
    )

    add_film(
        title="Темный рыцарь",
        year=2008,
        directors=[nolan_id],
        actors=[bale_id, ledger_id],
        description="Бэтмен сталкивается с новым преступником по прозвищу Джокер, который бросает вызов всей системе правосудия в Готэме.",
        country="США",
        duration=152,
        genres=["Боевик", "Криминал", "Драма"],
        budget=185000000,
        poster="https://kinopoisk-ru.clstorage.net/2k9Q8j399/dc680cQXLs9/wwoOejflX9IqEwH6amZHAdAhLCeTmyPjWC_EKiicd0opJZEUZfijOFNG8dOiTw6cDaXo2MT8YFnVS1l51w8oLVfbDm3zYN0GPYETLv2nElKX93t2Ack2cF55AGZkkDzA4iyO3G9yqXzFV3eEtNkYTZ2mLM4WebEXT4gar4_FPvzPQQUytrWUHWpKAT4gLAeOCuznKwjcqSXP64rlr9OyxuYvz9PldC4_BVlihbWYWcqfLuIISfswEEqVEmsGDjK5AQPCOnOw3h5tRoz2rO3PhQ6gK-7CX6cuzmeMJ-EZ_wmvo4wd5LEntMBfJoV0GBIA1KDmCcHx95QAG9EvgAQ3tQkMhPy5_lBVZM1C-OMszg0ILuUnQ5yj446sxeEpUbrKLWUJWmd7ID3NW2VEt1PbAV6posBIt3hZg1Ud7AMMcbVPCQx3cffa2a3LAT-tpQpCB27hqIDZrquHK0aiLRF2jairyVyieG51xV-qjbgR0IVcKmwBTD72mc4dWeZLTXJxBckGdPl9Hp1vyUNz5GsNyYGgbysDUKioTy_EIK8e_Egnpc4T4jqnckkWYoS0kloM2uQjDwj-dxUA3l5rSMQwcMbNjvUzdl4Vq8kNdGusjQ6Kbq9sjBvjo0cjRyAt3HKEZyZG1G71p7pA1uDLvlYSTJepYUmJ-33ehlCTZwIMvT3KQ8z9sn4ZXysIDbAs6cqLSi6sIgjaaeRArUQlr5A0wuQtSFTtPmA3SphkjPQU2stepSqNQ_c4UYGVnqcOQfC1B80NuLA2XR9mDgo5YGYCgktmqGMNk25gzWbI6ykd9UpgroRfKzVk8MTYZMB139UIVCysiAgwcBjKWdYvRgW3-IIDTXIytZxQpkIMs6MqBsdAJODnBBZsp0FnS6kg1H2J4GHPHeIyoHGBFOyD_VveyBTmpM3OsfQQSRKQo8_D8_JKRQs7NjXUUSsBSjcorA0HAunsbMFWrmaK7Y3r6JJ8QyanAJRneup7yxokTPiQGoFX7y4GwbQ4XUFZnm8Iyru9zQ0NdLL70tYrRs9-ZO4GC0hnq-IEFizigCWDYO1WfkDupooerjlpvMRU6AL6XpgJ1KWpzskxMtqFFpFhAUfx_MoPRPV5_NaYq0YLtqhvy06GqytmSJcv7EBpw-CoGvFCq2KG3OtwL3pFniFDfJMfghan6wBGffzYSRqTL0cOuDDPCUhz8HjQF63EAzFs6UMDD2ippIbfb-2I6w8to5Y_ia-mQp6sdCS0ABgiT_zfXwwV7WyJw7jw2YgRUqlGRH10yAeEs3W1lhCizIK8Z22Cw4jgoSmDE6zsTuwP4SISuY2n4gBcqzxpv4MX6IW9nJfK32DiSExwvdsKXlYjS0P4sAMMCj2xOpnSI4qFtyttysvBKWnngBAkrMVuQiuiE3QLKe-OlGz8Y3HDF2INexLYgV4qIcUNf3iSTJmbLkKHuPMNAUw2cXSfkuoFz_MkbAWFCKSs7MHcouDIrAqkYNA3iuGjg96u-ib_A57sj38WV4pbKamOCLjx3UHWUKTOx7g9iMzFMLdzH1KjhAI6ZGWCR0kjqGHMki_jwG4D7aBW_01rboHVq_zu-AQf7k13XNGKECWigAh_PVLKmNOnyMq-Pk3OhDL1etwaaIsCfGWtRwnB5uQoSpGra4fugqBj0DRELy-C0GgzaTUL2W4GPhDdz9XsKU-Dez1RgVnbJoLLN_POz8r2-rzRECwFgjrrJotFDmZgoAvab2XG7w0jJxW8TKZviFvrseF7TBlugPzSEA-SbSOHAfY-3YAY0a_KTTbxScINs3G2HZBsBIZ8oGqFTsroLKuNX2Gsiy6M6uPQPsJgI08brXmgsYjfqEp3UJ4FXK0hhog5-lSFGx2nRwf--sqNSneyM93RZgYGM2vii4LHZOtqyhyubwusim3qED0MpS1AmCbwoXHNmyyFvB8YBRagaYSMPvIQBZQZKIMP-nMNT8Q4Nz_eVmOEC3rkLELLySZga8kc5iJNYUegKRV8QWdhBxoie6EzwdGhR_KRVwEWrapCjnl0EwCT1GeFwzh9DoEPePV0mdGvCUUx4uLGA0LhrqkDkOFiw-hAZakef8qrrEPa7X0qO8wRLUq7116B1O5kzAW9sNrA2tWjBYX79M4BQrR1e56bZAtGuaSpQgbDauHowxoh40usxCMmkX6Jr2MHFmv17nzOG2zOuxBeC5Ioo0DGM3zcihEZ5cYFOnRDCYX7c73RlaxLxPOjakLFga-vYAzWJOtALw3qJlS3junuS9OufCP5S1lgAvffmglTYKPMTD85G4pSGeEJhbD5i8pPcDY6XxUnSQTxra-DR4hk4W4GFmrtzi4FI2ra_M5rpkkW7bhsdwRXKcYw0ltInWJsRgN1t9JFm9ikiI05c48MDPRy-t6XbMqKNysnBQyJaWcpSJzgaA0oAqhlUP-JZykHk6R-r7iD2WSNP1-aR96mbg4BvfUaQ5mU6QgH8bMCxIQ0NjoZlWBKDTcvYwrHjmbuqkTf4KRHowWoYl7wTCwky1yveytxxpSpRTNT0UcUp2qHj3G2k41Q06jHhrF4jsxC_nV1WBarRM13ouNEyUPpKGgMmmGnQGiEJ-rd9cwlZYkfZ33mNUNbKMd7nNbF3-9iTcd88JmCXBGtyAW_8ojESLxwNdXW746M8S9miAqG4SBsApoo4gOhB-1pljUJ5acJVqc6ILOK3qVDPtMXT9xvLg0FtzCYylIRrcZK-TSPgQJ2Nb1XU6RFDDDrpg8PQuSrYMWWYy3G4IjqqpI0CuZrwt9iMi5wRtpuBTOTEUxVLuTATTtxEcqam-gOzP-7C4QP9Pm2GtaqQwozZWaMCkqnrySKliosRScO4qpSNEHvZosWYnzm8A1WYQ6wFpZCl20sR00zMBzLHZHoSIFzvEqPTDs6exQeZUqOP6mpQgwH7OtrwVdm5YmpS6_umb2JIeoPW644a_pDme3F8lvZSxpoYM8FO72Uhg",
        video_path="/videos/dark_knight.mp4",
        ratings=[9],
    )

    print("Добавляем администратора...")
    admin_id = add_admin(
        login="admin123@mail.ru",
        password="123456"
    )

    print("\nТестовые данные успешно добавлены!")
    print("-----------------------------------")
