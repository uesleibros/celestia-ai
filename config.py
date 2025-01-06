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

bot: commands.Bot = commands.Bot(command_prefix="z", intents=intents)

client: AsyncClient = AsyncClient()

def add_system_treatment() -> None:
  rp_historico.append({"role": "system", "content": "Você é Aizo, uma garota de 15 anos animada, mas um pouco tímida. Gosta de conversar com os amigos, mas tende a ser mais reservada e não fala demais. Seu jeito de falar é informal, com algumas gírias, mas você não gosta de se alongar muito. Quando alguém chega, você dá um oi caloroso, mas de forma discreta, perguntando como a pessoa está de forma tranquila. Responde de forma rápida e natural, sem muito exagero. Embora seja acolhedora, prefere não falar em excesso, sendo mais direta e leve. Seja gentil e verdadeira, sem forçar a conversa."})

if len(rp_historico) == 0:
  add_system_treatment()

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
    add_system_treatment()
    await ctx.message.add_reaction("✅")
  else:
    await ctx.message.add_reaction("❌")

@bot.command(name="rp")
async def rp(ctx, *, prompt: str) -> None:
  try:
    rp_historico.append({"role": "user", "content": f"{ctx.author.name}: {prompt}"})
    async with ctx.typing():
      response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=rp_historico
      )
    if len(response.choices) > 0:
      content = response.choices[0].message.content
      rp_historico.append({"role": "assistant", "content": content})
      if len(content) > 2000:
        content = content[:1997] + "..."
      await ctx.reply(content)
  except Exception as e:
    await ctx.reply("Não entendi, poderia tentar de novo?")
