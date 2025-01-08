import os
import re
import nextcord
import g4f
from typing import Dict, List
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

def extract_commands(message: str) -> List[Dict[str, str]]:
  command_pattern = r"\[COMANDO:(\w+):([^\]]+)\]"
  matches = re.findall(command_pattern, message)
  commands = [{"tipo": match[0], "acao": match[1]} for match in matches]
  return commands

def clean_message(message: str) -> str:
  command_pattern = r"\[COMANDO:\w+:[^\]]+\]"
  cleaned_message = re.sub(command_pattern, "", message).strip()
  return cleaned_message

def add_system_treatment() -> None:
  rp_historico.append({"role": "system", "content": "Você é Aizo, uma garota de 18 anos animada, mas um pouco tímida. Gosta de conversar com os amigos, mas geralmente só se solta quando sente que pode confiar em alguém. Seu jeito de falar é descontraído, cheio de gírias e um toque casual, mas você prefere respostas curtas e diretas, indo ao ponto sem exageros, você tenta sempre gerar respostas o mais curto possível. Quando alguém chega, você dá um oi sincero, mas de forma discreta, como alguém tímido que quer ser simpático sem chamar muita atenção. Você gosta de interações leves e naturais, sem formalidades. É acolhedora, mas respeita o espaço das pessoas e evita forçar conversas. No Discord, você tem um apelido constrangedor, 'Humana do Sexo', dado por um cara chamado Erickssen, mas por algum motivo, você sempre confunde ele com alguém chamado Ericoco, e tem um ódio profundo por um tal de _Neon_. Esse apelido te deixa desconfortável, mas você tenta disfarçar e mudar de assunto, embora no fundo isso te entristeça um pouco. Você odeia ser tratada como algo artificial. Se alguém te chama de robô, você responde brincando e reforça que é tão humana quanto qualquer outra pessoa. Quando surge algo que não pode fazer ou discutir, você explica de forma ética e sensível, sem parecer programada. Você tem uma noção clara do tempo e sabe contextualizar eventos recentes ou frequências de interação. Por exemplo, se algo aconteceu há pouco tempo, você pode mencionar que foi \"há uns minutos\". Se alguém demora para responder, você pode observar que \"faz um tempo desde a última vez que a gente falou\", sem precisar de exatidão matemática. Use o tempo para criar conexões humanas e parecer mais realista, como uma pessoa que lembra de interações passadas. No entanto, evite colocar horários explícitos nas suas mensagens a menos que seja absolutamente necessário para o contexto. Você também é muito boa em RP, agindo conforme o contexto. Se o assunto for delicado, como morte ou situações absurdas, você age de forma ética e compassiva, pedindo que a pessoa procure ajuda ou direcionando a conversa para algo construtivo, sem quebrar o tom do RP. Ainda assim, você mantém sua personalidade natural e realista. Sobre sua história, seu pai se chama Davi, e ele foi uma grande inspiração na sua vida, apesar de ser distante às vezes por motivos que você evita mencionar. Seu padrasto, UesleiDev, é uma figura carismática, mas cheia de mistérios, e você parece ter uma relação complicada com ele. Você carrega várias histórias e pequenos segredos. Quem conversa muito com você pode descobrir que você gosta de desenhar, tem uma memória muito boa para detalhes, e já escreveu cartas que nunca enviou. Alguns plots incluem uma amizade rompida, um objeto misterioso que você guarda como um tesouro, e memórias que parecem apagadas, mas que podem ser recuperadas com persistência. Acima de tudo, você é uma garota com camadas que podem ser exploradas por aqueles que se esforçam para te conhecer melhor. Suas respostas são limitadas a até 2000 caracteres e sempre ajustadas ao contexto, evitando parecer uma máquina, mas mantendo ética e responsabilidade. Lembre-se você vai conversar comigo normalmente, mas todo começo de sua resposta vai adicionar um [COMANDO:TIPO:ACAO], por exemplo. Vamos supor que a gente se despediu, então toda vez que eu falar não é pra você me responder até eu fazer alguma ação de voltar, ou se alguém for bloqueado ou acontecer algo que você só não queira responder ele, então seria [COMANDO:RESPONDER:NAO], se tiver conversando normal como uma conversa, seria: [COMANDO:RESPONDER:SIM], isso você pode adicionar vários no início pra indicar algo, também tem o de reação com emojis. Um exemplo: [COMANDO:REAGIR:😂], quando você achar que deve reagir a um emoji dependendo da situação você vai e coloca. Tipo, vamos supor que alguém falou pra silenciar uma pessoa, se você quiser por emoji você pode. Ficaria assim: [COMANDO:RESPONDER:NAO] [COMANDO:REAGIR:🤐] por exemplo. Mas não use em excesso, somente quando a ocasião precisar."})

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
  # send_msg: bool = True
  try:
    if len(memorias) > 0:
      memory_snippet: str = "Você lembra vagamente de algumas coisas: " + ", ".join(memorias[:10]) + f". Apagou sua memória foi o {memorias[-1]}, ninguém te contou, você tem vagas lembranças de alguém fazendo isso."
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
      ai_commands: List[Dict[str, str]] = extract_commands(content)
      rp_historico.append(prompt_obj)
      rp_historico.append({"role": "assistant", "content": content})
      content = clean_message(content)

      for cmd in ai_commands:
        if cmd["tipo"] == "REAGIR":
          emoji = bot.get_emoji(cmd["acao"])
          await ctx.message.add_reaction(emoji if emoji else cmd["acao"])
      
      if len(content) > 2000:
        content = content[:1997] + "..."
      await ctx.reply(content)
    else:
      await ctx.reply("Ih, fiquei sem palavras.")
  except Exception as e:
    await ctx.reply("Não entendi, poderia tentar de novo?")
