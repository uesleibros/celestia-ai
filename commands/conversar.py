import g4f
from nextcord import Interaction, SlashOption, Attachment
from nextcord.ext import commands
from config import bot, client
from structures.text_models import TEXT_MODELS
from typing import Any
from utils.historico import historico

@bot.slash_command(
  name="conversar",
  description="Converse comigo, estou pronta para o que der e vier ☺."
)
async def conversar(
  interaction: Interaction,
  prompt: str = SlashOption(
    name="prompt",
    description="O que quer saber?",
    required=True
  ),
  modelo: str = SlashOption(
    name="modelo",
    description="Escolha o modelo de IA.",
    choices=TEXT_MODELS,
    default="gpt-4o"
  ),
  imagem: Attachment = SlashOption(
    name="imagem",
    description="Adicione uma imagem se deseja utilizá-la em seu prompt.",
    required=False
  )
):
  await interaction.response.defer(ephemeral=False)

  if interaction.user.id not in historico:
    historico[interaction.user.id] = []

  historico[interaction.user.id].append({"role": "user", "content": prompt})
  provider: Any = None

  if imagem:
    image_bytes = await imagem.read()
    provider = g4f.Provider.Blackbox

  try:
    response = await client.chat.completions.create(
      model=modelo,
      messages=historico[interaction.user.id],
      image=image_bytes if imagem else None,
      provider=provider,
      web_search=False,
    )
    if len(response.choices) > 0:
      content = response.choices[0].message.content
      historico[interaction.user.id].append({"role": "assistant", "content": content})

      header = f"{interaction.user.mention} Modelo escolhido: **{modelo}**\n"
      available_space = 2000 - len(header)
      if len(content) > available_space:
        content = content[:available_space - 1] + "—"

      await interaction.followup.send(header + content)
    else:
      await interaction.followup.send("Erro: nenhuma resposta obtida.")
  except Exception as e:
    await interaction.followup.send(f"Ocorreu um erro: {str(e)}")