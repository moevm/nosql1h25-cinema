import requests
from datetime import datetime

def fetch_wikidata_person_info(name):
    """Получает данные о персоне из Wikidata по имени"""
    # 1. Поиск ID персоны по имени
    search_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={name}&language=ru&format=json"
    search_res = requests.get(search_url).json()
    
    if not search_res.get("search"):
        return None
    
    person_id = search_res["search"][0]["id"]
    
    # 2. Получение данных о персоне по ID
    query = f"""
    SELECT ?person ?personLabel ?birthDate ?birthPlaceLabel ?photo WHERE {{
      wd:{person_id} wdt:P31 wd:Q5;
              rdfs:label ?personLabel.
      FILTER(LANG(?personLabel) = "ru").
      OPTIONAL {{ wd:{person_id} wdt:P569 ?birthDate. }}
      OPTIONAL {{ wd:{person_id} wdt:P19 ?birthPlace. }}
      OPTIONAL {{ wd:{person_id} wdt:P18 ?photo. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru". }}
    }}
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "YourApp/1.0",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params={"query": query, "format": "json"})
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]["bindings"]:
            result = data["results"]["bindings"][0]
            return {
                "name": result["personLabel"]["value"],
                "birth_date": result.get("birthDate", {}).get("value"),
                "birth_place": result.get("birthPlaceLabel", {}).get("value"),
                "photo_url": result.get("photo", {}).get("value"),
                "wiki_link": f"https://www.wikidata.org/wiki/{person_id}"
            }
    return None