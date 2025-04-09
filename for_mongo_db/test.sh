#!/bin/bash

API_URL="http://localhost:5000"

# Добавляем режиссера
echo "Добавляем режиссера..."
director_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "name": "Christopher Nolan",
    "role": "director",
    "birth_date": "1970-07-30",
    "birth_place": "London, England",
    "wiki_link": "https://en.wikipedia.org/wiki/Christopher_Nolan"
}' "$API_URL/api/persons")

director_id=$(echo "$director_response" | jq -r '.id')
echo "Режиссер добавлен с ID: $director_id"

# Добавляем актера
echo "Добавляем актера..."
actor_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "name": "Leonardo DiCaprio",
    "role": "actor",
    "birth_date": "1974-11-11",
    "birth_place": "Los Angeles, USA",
    "wiki_link": "https://en.wikipedia.org/wiki/Leonardo_DiCaprio"
}' "$API_URL/api/persons")

actor_id=$(echo "$actor_response" | jq -r '.id')
echo "Актер добавлен с ID: $actor_id"

# Добавляем фильм
echo "Добавляем фильм..."
curl -X POST -H "Content-Type: application/json" -d '{
    "title": "Inception",
    "year": 2010,
    "directors": ["'$director_id'"],
    "actors": ["'$actor_id'"],
    "description": "A thief who steals corporate secrets through dream-sharing technology",
    "country": "USA",
    "duration": 148,
    "genres": ["sci-fi", "action"],
    "budget": 160000000,
    "poster": "inception.jpg",
    "video_path": "/videos/inception.mp4"
}' "$API_URL/api/films"

echo -e "\nТестовые данные успешно добавлены!"
echo "-----------------------------------"
echo "Фильм: Inception (2010)"
echo "Режиссер: Christopher Nolan ($director_id)"
echo "Актер: Leonardo DiCaprio ($actor_id)"