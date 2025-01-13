import os
import re
import nextcord
import g4f
from utils.historico import historico, rp_historico, memorias
from utils.rp.start_sys_prompt import add_system_treatment
from dotenv import load_dotenv
from nextcord.ext import commands
from g4f.client import AsyncClient
from g4f.cookies import set_cookies

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
_U_TOKEN: str = os.getenv("_U")

set_cookies(".bing.com", {
  "_U": _U_TOKEN
})

intents: nextcord.Intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix="z", intents=intents)
client: AsyncClient = AsyncClient()

if len(rp_historico) == 0:
  add_system_treatment()

