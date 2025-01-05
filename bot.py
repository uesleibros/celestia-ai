from flask import Flask
from config import bot

app: Flask = Flask(__name__)

def run_flask_app() -> None:
  app.run(host="0.0.0.0", port=8080)

from commands import conversar, imaginar, criar_variacao