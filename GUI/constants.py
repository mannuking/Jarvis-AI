import os
from kivy.config import Config

width, height = 1920, 1080

Config.set('graphics','width',width)
Config.set('graphics','height',height)
Config.set('graphics','fullscreen','True')

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

IP_ADDR_API_URL = os.environ.get("IP_ADDR_API_URL")
NEWS_FETCH_API_URL = os.environ.get("NEWS_FETCH_API_URL")
NEWS_FETCH_API_KEY = os.environ.get("NEWS_FETCH_API_KEY")
# Weather API constants
WEATHER_FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_FORECAST_API_KEY = "5bb7a24dce6705d0f545a684ddf42a12"  # Replace this with your actual API key
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")


SMTP_URL = os.environ.get("SMTP_URL")
SMTP_PORT = os.environ.get("SMTP_PORT")

SCREEN_WIDTH = Config.getint('graphics','width')
SCREEN_HEIGHT = Config.getint('graphics','height')


