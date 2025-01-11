#from threading import Thread
from bot import bot, run_flask_app
from config import TOKEN

if __name__ == "__main__":
  #Thread(target=run_flask_app, daemon=True).start()
  bot.run(TOKEN)