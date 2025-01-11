import nextcord
import asyncio
from config import client, bot
from utils.rp.image import analyze_image
from utils.rp.commands import extract_commands, clean_message
from utils.historico import memorias, rp_historico, system_context, rp_modelo
from utils.rp.sys_context import create_system_context
from datetime import datetime, timedelta

@bot.event
async def on_message(message: nextcord.Message) -> None:
  global system_context
  if message.author.bot:
    return

  if not message.content.startswith("zrp "):
    await bot.process_commands(message)
    return
    
  permissions: object = message.channel.permissions_for(message.guild.me)
  if not permissions.send_messages:
    return

  send_msg: bool = True
  prompt: str = message.content[4:].strip()

  if len(prompt) == 0:
    return
  try:
    if len(memorias) > 0:
      memory_snippet: str = "Você lembra vagamente de algumas coisas: " + ", ".join(memorias[:10]) + f". Apagou sua memória foi o {memorias[-1]}, ninguém te contou, você tem vagas lembranças de alguém fazendo isso."
      rp_historico.insert(1, {"role": "system", "content": memory_snippet})
      memorias.clear()
    current_time: str = (datetime.utcnow() - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M:%S")

    image_bytes: bytes = None
    image_response: str = None
    if message.attachments:
      image_bytes = await message.attachments[0].read()
      image_response = await analyze_image(prompt, image_bytes)
      if image_response:
        prompt = f"Interprete isso (isso são dados de uma imagem completamente analisada): '{image_response}'. Agora, voltando para o assunto, o que você acha disso? Pergunta feita: {prompt}."

    prompt_obj: Dict[str, str] = {
      "role": "user",
      "content": f"[{current_time}] {message.author.name} "
                 f"(ID: {message.author.id} | SERVIDOR: {message.guild.name} | CANAL ID: {message.channel.id} | "
                 f"FOTO DE PERFIL: {message.author.avatar.url if message.author.avatar else 'Nenhuma'} | "
                 f"FOTO DE PERFIL DO SERVIDOR: {message.author.guild_avatar.url if message.author.guild_avatar else 'Nenhuma'} | "
                 f"CARGOS: {', '.join([role.name for role in message.author.roles])} | "
                 f"ATIVIDADES: {', '.join([str(activity) for activity in message.author.activities]) if message.author.activities else 'Nenhuma'}): {prompt}"
    }

    if not system_context:
      system_context = await create_system_context(message.guild)

    system_context_object = {
      "role": "system",
      "content": f"Contexto atual do servidor, use essas informações quando precisar:\n{system_context}"
    }
    response: object = await client.chat.completions.create(
      model=rp_modelo,
      messages=[system_context_object] + rp_historico + [prompt_obj],
      max_tokens=200
    )

    if len(response.choices) > 0:
      content = response.choices[0].message.content
      ai_commands: List[Dict[str, str]] = extract_commands(content)
      rp_historico.append(prompt_obj)
      rp_historico.append({"role": "assistant", "content": content})
      content = clean_message(content)

      tasks = []

      for cmd in ai_commands:
        if cmd["tipo"] == "RESPONDER" and cmd["acao"] == "NAO":
          send_msg = False
        elif cmd["tipo"] == "REAGIR":
          emoji = bot.get_emoji(cmd["acao"])
          task = asyncio.create_task(add_reaction(message, emoji if emoji else cmd["acao"]))
           tasks.append(task)

      if len(content) > 2000:
        content = content[:1997] + "..."

      try:
        if send_msg and len(content.strip()) > 0:
          task_send_msg = asyncio.create_task(message.reply(content))
          tasks.append(task_send_msg)

        await asyncio.gather(*tasks)
      except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    else:
      await message.reply("Ih, fiquei sem palavras.")
  except Exception as e:
    await message.reply("Não entendi, poderia tentar de novo?" + str(e))

async def add_reaction(message: nextcord.Message, emoji: str) -> None:
  try:
    await message.add_reaction(emoji)
  except Exception as e:
    pass