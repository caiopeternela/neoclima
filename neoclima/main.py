import typer
import requests
from tinydb import TinyDB, Query
import os
from dotenv import load_dotenv
from neoclima.commands_svc import get_emoji
load_dotenv()

app = typer.Typer()

db = TinyDB("db.json")

API_KEY = os.getenv("API_KEY")

@app.command()
def now(city_nickname: str):
    """
    Check current weather for the given city nickname
    """
    city = db.search(Query().city == city_nickname)
    if city:
        lat = city[0]["coordinates"][0]
        lon = city[0]["coordinates"][1]
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&units=metric&lon={lon}&limit=1&appid={API_KEY}")
        content = r.json()
        current_temperature = int(content["main"]["temp"])
        weather = content["weather"][0]["main"]
        emoji = get_emoji(weather)
        print(emoji + "  " + str(current_temperature) + "°C")
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
        state = input("Type the state code (only for US): ")
        city = input("Type the city name: ")
        r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={API_KEY}")
        lat = r.json()[0]["lat"]
        lon = r.json()[0]["lon"]
        db.insert({"city": city_nickname, "coordinates": [lat,lon]})
        print("City added succesfully!")
    else:
        print("City already added!")


@app.command()
def edit(city_nickname: str):
    """
    Edit city nickname
    """
    city_nickname_db = db.search(Query().city == city_nickname)
    if city_nickname_db:
        new_city_nickname = input(f'Type the new city nickname for "{city_nickname}": ')
        db.update({"city": new_city_nickname}, Query().city == city_nickname_db[0]["city"])
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
    cities_nicknames = [dict["city"] for dict in db]
    print(*cities_nicknames, sep="\n")
