from flask import Flask
from config import bot

app: Flask = Flask(__name__)

def run_flask_app() -> None:
  app.run(host="0.0.0.0", port=8080)

from commands.slash import conversar, imaginar
from events.on_message import on_message
from commands.text import *