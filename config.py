import os
import nextcord
from utils.historico import historico
from dotenv import load_dotenv
from nextcord.ext import commands
from g4f.client import AsyncClient

load_dotenv()

TOKEN: str = os.getenv("TOKEN")

intents: nextcord.Intents = nextcord.Intents.default()
intents.message_content = True

bot: commands.Bot = commands.Bot(command_prefix="c.", intents=intents)
@bot.command(name="clshist")
async def _limpar_historico(ctx):
	if ctx.author.id in historico:
		del historico[ctx.author.id]
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")

client: AsyncClient = AsyncClient()