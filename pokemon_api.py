# pokemon_api.py
import requests

def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "type": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "image": data["sprites"]["front_default"]  # Añadir la imagen
        }
    else:
        return None

def fetch_pokemon_list():
    """Obtiene la lista de nombres de Pokémon desde la PokéAPI."""
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [pokemon["name"] for pokemon in data["results"]]
    
    return []