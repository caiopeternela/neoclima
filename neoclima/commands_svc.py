import emoji

def get_emoji(weather: str):
    weather_emojis = {
        "Clouds": emoji.emojize(":cloud:"),
        "Rain": emoji.emojize(":cloud_with_rain:"),
        "Clear": emoji.emojize(":sun:")
    }
    return weather_emojis[weather]