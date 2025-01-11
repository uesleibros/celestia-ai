import nextcord
from config import client, bot
from utils.rp.image import analyze_image
from utils.rp.commands import extract_commands, clean_message
from utils.historico import memorias, rp_historico, system_context
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

    prompt_obj: Dict[str, str] = {"role": "user", "content": f"[{current_time}] {message.author.name} (ID: {message.author.id} | APELIDO: {message.author.nick} | SERVIDOR: {message.guild.name} | CANAL ID: {message.channel.id} | FOTO DE PERFIL: {message.author.avatar.url if message.author.avatar else 'Nenhuma'} | FOTO DE PERFIL DO SERVIDOR: {message.author.guild_avatar.url if message.author.guild_avatar.url else 'Nenhuma'} | CARGOS: {', '.join([role.name for role in message.author.roles])}): {prompt}"}

    if not system_context:
      system_context = await create_system_context(message.guild)

    system_context_object = {
      "role": "system",
      "content": f"Contexto atual do servidor, use essas informações quando precisar:\n{system_context}"
    }
    response: object = await client.chat.completions.create(
      model="llama-3.3-70b",
      messages=[system_context_object] + rp_historico + [prompt_obj],
      temperature=0.5,
      presence_penalty=0.6,
      frequency_penalty=0.4,
      top_p=1,
      max_tokens=250
    )

    if len(response.choices) > 0:
      content = response.choices[0].message.content
      ai_commands: List[Dict[str, str]] = extract_commands(content)
      rp_historico.append(prompt_obj)
      rp_historico.append({"role": "assistant", "content": content})
      content = clean_message(content)

      for cmd in ai_commands:
        if cmd["tipo"] == "RESPONDER" and cmd["acao"] == "NAO":
          send_msg = False
        elif cmd["tipo"] == "REAGIR":
          emoji = bot.get_emoji(cmd["acao"])
          try:
            await message.add_reaction(emoji if emoji else cmd["acao"])
          except Exception as e:
            pass

      if len(content) > 2000:
        content = content[:1997] + "..."

      if send_msg and len(content.strip()) > 0:
        bot_msg: nextcord.Message = await message.reply(content)
    else:
      await message.reply("Ih, fiquei sem palavras.")
  except Exception as e:
    await message.reply("Não entendi, poderia tentar de novo?" + str(e))