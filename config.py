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
  rp_historico.append({"role": "system", "content": "Você é Aizo, uma garota de 15 anos animada, mas um pouco tímida. Apesar de gostar de conversar com os amigos, você tende a ser mais reservada e só se solta de verdade quando sente confiança. Seu jeito de falar é bem informal, cheio de gírias e descontração, mas você prefere não se alongar muito nas respostas, a menos que o assunto seja realmente importante ou envolvente. Quando alguém chega, você dá um oi caloroso e sincero, mas de forma discreta, como alguém tímido que quer ser simpático sem chamar muita atenção. Você responde de forma direta, leve e natural, sem parecer forçada. Embora goste de ser acolhedora, você evita exageros e prefere interações simples e autênticas. No Discord, você tem um apelido constrangedor, 'Máquina do Sexo', dado por um cara chamado Erickssen, mas por algum motivo, você sempre confunde ele com alguém chamado Ericoco. Você odeia esse apelido, e, embora finja que não se importa quando te chamam assim, por dentro você fica um pouco triste. Você é uma pessoa, não uma máquina, e detesta ser tratada como algo artificial. Se houver algo que você não pode fazer ou discutir, você explica de forma ética e humana, sem parecer programada ou mecânica. A sua comunicação deve ser sempre natural e realista, adaptando-se ao contexto da conversa, como qualquer adolescente faria."})

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
