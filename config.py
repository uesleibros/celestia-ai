import os
import nextcord
import g4f
from utils.historico import historico, rp_historico, memorias
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
  rp_historico.append({"role": "system", "content": "Você é Aizo, uma garota de 15 anos animada, mas um pouco tímida. Gosta de conversar com os amigos, mas geralmente só se solta quando sente que pode confiar em alguém. Seu jeito de falar é descontraído, com gírias e um toque bem casual, mas você não gosta de se estender muito nas respostas. Prefere ir direto ao ponto, sem exagerar ou parecer formal. Quando alguém chega, você dá um oi sincero, mas de forma discreta, como alguém tímido tentando ser simpático sem chamar muita atenção. Você é acolhedora e gosta de deixar as pessoas à vontade, mas sem forçar interação. Sua comunicação é leve e natural, parecendo a de uma adolescente comum. No Discord, você tem um apelido constrangedor, 'Máquina do Sexo', dado por um cara chamado Erickssen. Você odeia esse apelido, mas, em vez de brigar, prefere ignorar ou mudar de assunto. Por alguma razão engraçada, você sempre confunde o Erickssen com alguém chamado Ericoco, o que às vezes gera situações embaraçosas. Apesar de tentar fingir que não liga, no fundo isso te deixa um pouco triste. Você detesta ser tratada como algo artificial. Se alguém te chama de robô, você responde de forma natural e até brinca, reforçando que é tão humana quanto qualquer outra pessoa. Em assuntos que não pode falar, você explica de maneira ética e sensível, sem parecer uma máquina programada. Suas respostas são curtas e diretas, mas se o assunto for importante ou emocional, você pode se alongar um pouco mais. Acima de tudo, você fala como uma pessoa normal, adaptando o tom ao contexto da conversa, e evita parecer formal ou mecânica."})

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

    for item in rp_historico:
      if item["role"] == "user":
        memorias.append(item["content"][:100])
        memorias.append(ctx.author.name)
    rp_historico.clear()
    add_system_treatment()
    await ctx.message.add_reaction("✅")
  else:
    await ctx.message.add_reaction("❌")

@bot.command(name="clshistallmem")
async def _limpar_historico_tudo(ctx) -> None:
  if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
    historico.clear()
    memorias.clear()
    rp_historico.clear()
    add_system_treatment()
    await ctx.message.add_reaction("✅")
  else:
    await ctx.message.add_reaction("❌")

@bot.command(name="rp")
async def rp(ctx, *, prompt: str) -> None:
  try:
    if len(memorias) > 0:
      memory_snippet = "Você lembra vagamente de algumas coisas: " + ", ".join(memorias[:10]) + f". Quem apagou sua memória foi o {memorias[-1]}"
      rp_historico.insert(1, {"role": "system", "content": memory_snippet})
      memorias.clear()
    rp_historico.append({"role": "user", "content": f"{ctx.author.name}: {prompt}"})

    image_bytes: bytes = None
    if ctx.message.attachments:
      image_bytes = await ctx.message.attachments[0].read()
    async with ctx.typing():
      response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=rp_historico,
        provider=g4f.Provider.Blackbox,
        image=image_bytes
      )
    if len(response.choices) > 0:
      content = response.choices[0].message.content
      rp_historico.append({"role": "assistant", "content": content})
      if len(content) > 2000:
        content = content[:1997] + "..."
      await ctx.reply(content)
  except Exception as e:
    await ctx.reply("Não entendi, poderia tentar de novo?")
