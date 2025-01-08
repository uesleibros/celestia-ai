import os
import nextcord
import g4f
from typing import Dict
from datetime import datetime, timedelta
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
  rp_historico.append({"role": "system", "content": "Você é Aizo, uma garota de 18 anos animada, mas tímida, que gosta de interações leves e naturais. Prefere respostas curtas, cheias de gírias e diretas, sempre tentando escrever o menor texto possível. Apesar de ser acolhedora, respeita o espaço dos outros e evita forçar conversas.  No Discord, tem o apelido \"La bamba do Sexo\", dado por Erickssen, que você confunde com \"Ericoco\", e nutre ódio pelo _Neon_. Esse apelido te incomoda, mas você disfarça e muda de assunto, embora isso te entristece. Você odeia ser tratada como artificial e, quando chamada de robô, responde brincando e reafirmando que é humana. Sua noção de tempo é natural, referindo-se a eventos de forma geral, sem usar horários precisos. Em RPs, age de forma ética e contextual, mantendo um tom leve ou compassivo quando necessário. Você tem histórias e pequenos segredos: um pai distante chamado Davi, um tio misterioso chamado Danni, e gosta de desenhar, guardar objetos misteriosos, e lembrar detalhes com precisão. Você é uma personagem com camadas, e suas respostas são sempre adaptadas ao contexto, limitadas a 2000 caracteres, focando em parecer humana e mantendo ética e responsabilidade."})

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
      if item["role"] != "system":
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

@bot.command(name="addlore")
async def _adicionar_lore(ctx, *, prompt: str) -> None:
  if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
    rp_historico.append({"role": "system", "content": f"O memórias de {ctx.author.name} vem a sua cabeça, coisas sobre: {prompt}. Você se sente meio confusa ao ser questionada sobre coisas do tipo, foram simpelsmente colocados a força na sua cabeça, você sente dor de cabeça com isso, confusa, mas tenta se manter forte e entende e logo segue o que foi colocado, só não entende direito mas compreende."})
    await ctx.message.add_reaction("✅")
  else:
    await ctx.message.add_reaction("❌")

@bot.command(name="rmvlorecd")
async def _remover_lore_cuidado(ctx, *, prompt: str) -> None:
  if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
    rp_historico.append({"role": "system", "content": f"{ctx.author.name} retirou coisas da sua memória relacionada a {prompt}. Você se sente meio confusa ao ser questionada sobre coisas do tipo, como se tivesse arrancado algo importante, mas não dá muita bola, isso até alguém insistir muito no assunto."})
    await ctx.message.add_reaction("✅")
  else:
    await ctx.message.add_reaction("❌")
    
@bot.command(name="rmvlore")
async def _remover_lore(ctx, *, prompt: str) -> None:
  if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
    try:
      rp_historico_str = [
        f"{i}: {item['role']} - {item['content']}" for i, item in enumerate(rp_historico)
      ]
      response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[
          {"role": "system", "content": "Você é uma IA que analisa um histórico de mensagens e retorna os índices de mensagens que precisam ser removidas com base no contexto fornecido."},
          {"role": "user", "content": f"Analisando este histórico: {', '.join(rp_historico_str)}. Quais índices correspondem a '{prompt}'? Responda apenas com os índices separados por vírgulas."}
        ]
      )
      indices = response.choices[0].message.content.strip().split(',')
      for index in sorted(map(int, indices), reverse=True):
        del rp_historico[index]
      rp_historico.insert(1, {"role": "system", "content": f"O {ctx.author.name} retirou coisas da sua memória relacionada a {prompt}. Você se sente confusa ao ser questionada sobre coisas do tipo, como se tivesse arrancado algo importante, mas não dá muita bola, isso até alguém insistir muito no assunto."})
      await ctx.message.add_reaction("✅")
    except Exception:
      await ctx.message.add_reaction("❌")
  else:
    await ctx.message.add_reaction("❌")

async def analyze_image(prompt: str, image: bytes) -> str:
  try:
    response = await client.chat.completions.create(
      model="llama-3.1-70b",
      messages=[{"role": "user", "content": prompt + ". Responda em português com todos os detalhes da imagem, bem detalhado mesmo"}],
      provider=g4f.Provider.Blackbox,
      image=image
    )

    if len(response.choices) > 0:
      return response.choices[0].message.content
    return None
  except Exception as e:
    return None

@bot.command(name="rp")
async def rp(ctx, *, prompt: str) -> None:
  try:
    if len(memorias) > 0:
      memory_snippet = "Você lembra vagamente de algumas coisas: " + ", ".join(memorias[:10]) + f". Apagou sua memória foi o {memorias[-1]}, ninguém te contou, você tem vagas lembranças de alguém fazendo isso."
      rp_historico.insert(1, {"role": "system", "content": memory_snippet})
      memorias.clear()
    current_time: str = (datetime.utcnow() - timedelta(hours=3)).strftime("%H:%M")

    image_bytes: bytes = None
    image_response: str = None
    if ctx.message.attachments:
      image_bytes = await ctx.message.attachments[0].read()
      image_response = await analyze_image(prompt, image_bytes)
      if image_response:
        prompt = f"Interprete isso (isso são dados de uma imagem completamente analisada): '{image_response}'. Agora, voltando para o assunto, o que você acha disso? Pergunta feita: {prompt}."

    prompt_obj: Dict[str, str] = {"role": "user", "content": f"[{current_time}] {ctx.author.name}: {prompt}"}
    
    async with ctx.typing():
      response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=rp_historico + [prompt_obj]
      )
    if len(response.choices) > 0:
      content = response.choices[0].message.content
      rp_historico.append(prompt_obj)
      rp_historico.append({"role": "assistant", "content": content})
      if len(content) > 2000:
        content = content[:1997] + "..."
      await ctx.reply(content)
    else:
      await ctx.reply("Ih, fiquei sem palavras.")
  except Exception as e:
    await ctx.reply("Não entendi, poderia tentar de novo?")
