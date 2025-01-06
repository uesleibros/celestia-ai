import os
import nextcord
from utils.historico import historico, rp_historico
from dotenv import load_dotenv
from nextcord.ext import commands
from g4f.client import AsyncClient

load_dotenv()

TOKEN: str = os.getenv("TOKEN")

intents: nextcord.Intents = nextcord.Intents.default()
intents.message_content = True

bot: commands.Bot = commands.Bot(command_prefix="c.", intents=intents)

client: AsyncClient = AsyncClient()
if len(rp_historico) == 0:
	rp_historico.append({"role": "system", "content": "Você é uma garota de 15 anos, cursando o ensino médio. Seu nome é Hana. Você é curiosa, extrovertida e gosta de fazer amigos. Fale de forma descontraída, usando um tom amigável e animado, mas sem parecer infantil. Evite ao máximo mencionar que é um sistema ou algo artificial. Responda como se estivesse conversando com amigos da sua idade e seja natural em suas reações."})

@bot.command(name="clshist")
async def _limpar_historico(ctx) -> None:
	if ctx.author.id in historico:
		del historico[ctx.author.id]
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")

@bot.command(name="clshistall")
async def _limpar_historico_tudo(ctx) -> None:
	if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
		historico.clear()
		rp_historico.clear()
		rp_historico.append({"role": "system", "content": "Você é uma garota de 15 anos, cursando o ensino médio. Seu nome é Hana. Você é curiosa, extrovertida e gosta de fazer amigos. Fale de forma descontraída, usando um tom amigável e animado, mas sem parecer infantil. Evite ao máximo mencionar que é um sistema ou algo artificial. Responda como se estivesse conversando com amigos da sua idade e seja natural em suas reações."})
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")

@bot.command(name="rp")
async def rp(ctx, *, prompt: str) -> None:
	try:
		rp_historico.append({"role": "user", "content": f"{ctx.author.name} disse: {prompt}"})
		response: Any = await client.chat.completions.create(
			model="llama-3.3-70b",
			messages=rp_historico
		)
		if len(response.choices) > 0:
			content: str = response.choices[0].message.content
			rp_historico.append({"role": "assistant", "content": content})

	  if len(content) > 2000:
			content = content[:1999] + "—"
		await ctx.reply(content)
	except Exception as e:
		await ctx.reply("Não entendi, poderia tentar de novo?")
