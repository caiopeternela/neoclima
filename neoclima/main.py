import typer
import requests
from tinydb import TinyDB, Query

app = typer.Typer()

db = TinyDB("./db.json")

@app.command()
def now(city_nickname: str):
    """
    Check current weather for the given city nickname
    """
    city = db.search(Query().city == city_nickname)
    if city:
        lat = city[0]["coordinates"][0]
        lon = city[0]["coordinates"][1]
        r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True")
        current_temperature = int(r.json()["current_weather"]["temperature"])
        print(str(current_temperature) + "°C")
    else:
        print("City not added!")


@app.command()
def add(city_nickname: str):
    """
    Add city with the given nickname
    """
    city_nickname_exists = bool(db.search(Query().city == city_nickname))
    if not city_nickname_exists:
        country = input("Type the country name or code (ISO3166): ")
        city = input("Type the city name: ")
        r = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?country_code={country}&name={city}&count=1")
        lat = r.json()["results"][0]["latitude"]
        lon = r.json()["results"][0]["longitude"]
        db.insert({"city": city_nickname, "coordinates": [lat,lon]})
        print("City added succesfully!")
    else:
        print("City already added!")


@app.command()
def edit(city_nickname: str):
    """
    Edit city nickname
    """
    city = db.search(Query().city == city_nickname)
    if city:
        new_city_nickname = input(f'Type the new city nickname for "{city_nickname}": ')
        db.update({"city": new_city_nickname}, Query().city == city[0]["city"])
        print("City nickname updated succesfully!")
    else:
        print("City not added!")


@app.command()
def rm(city_nickname: str):
    """
    Remove city
    """
    city_nickname_exists = bool(db.search(Query().city == city_nickname))
    if city_nickname_exists:
        db.remove(Query().city == city_nickname)
        print("City removed succesfully!")
    else:
        print("City not added!")


@app.command()
def ls():
    """
    List added cities
    """
    cities_nicknames = [d["city"] for d in db]
    if cities_nicknames:
        print(*cities_nicknames, sep="\n")
    else:
        print("No cities added!")
