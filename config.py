from dotenv import load_dotenv
from typing import Dict, Union, List, Any
from g4f.client import AsyncClient
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.errors import HTTPException
from flask import Flask
import threading
import nextcord
import os
import io
import aiohttp
import json
import uuid
import random

load_dotenv()

TOKEN: str = os.environ["TOKEN"]
intents: nextcord.Intents = nextcord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="c.", intents=intents)
client: AsyncClient = AsyncClient()
app = Flask(__name__)

@bot.event
async def on_ready():
	print(f"Bot conectado como {bot.user}.")

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
		choices={
			"GPT-4": "gpt-4",
			"GPT-4o": "gpt-4o",
			"LLAMA 2-7b": "llama-2-7b",
			"LLAMA 3.1-8b": "llama-3.1-8b",
			"LLAMA 3.1-70b": "llama-3.1-70b",
			"LLAMA 3.2-11b": "llama-3.2-11b",
			"LLAMA 3.3-70b": "llama-3.3-70b",
			"Mixtral 7b": "mixtral-7b",
			"Hermes 2 DPO": "hermes-2-dpo",
			"Hermes 2 Pro": "hermes-2-pro",
			"Gemini 1.5 Pro": "gemini-1.5-pro",
			"Gemini 1.5 Flash": "gemini-1.5-flash",
			"Claude 3.5 Sonnet": "claude-3.5-sonnet",
			"Openchat 3.5": "openchat-3.5",
			"DeepSeek Chat": "deepseek-chat",
			"DeepSeek Coder": "deepseek-coder"
		}
	)
) -> None:
	await interaction.response.defer(ephemeral=False)

	if interaction.user.id not in historico:
		historico[interaction.user.id] = []

	historico[interaction.user.id].append({"role": "user", "content": prompt})
	view: InterrupcaoView = InterrupcaoView(interaction)
	cancelar_resposta[interaction.user.id] = False

	response: object = await client.chat.completions.create(
		model=modelo,
		messages=historico[interaction.user.id],
		web_search=False
	)

	if len(response.choices) > 0:
		historico[interaction.user.id].append({"role": "assistant", "content": response.choices[0].message.content})
		await interaction.followup.send(f"{interaction.user.mention} {response.choices[0].message.content}")

@bot.slash_command(
	name="imaginar",
	description="Gere a imagem dos seus sonhos ☺.",
)
async def imaginar(
	interaction: Interaction,
	prompt: str = SlashOption(
		name="prompt",
		description="Descreva o que você quer que o modelo gere.",
		required=True
	),
	modelo: str = SlashOption(
		name="modelo",
		description="Escolha o modelo de IA.",
		choices={
			"Midjourney": "midjourney",
			"Any-Dark": "any-dark",
			"Dall-E-3": "dall-e-3",
			"SDXL": "sdxl",
			"SD-3": "sd-3",
			"Flux": "flux",
			"Flux Pro": "flux-pro",
			"Flux Dev": "flux-dev",
			"Flux Schnell": "flux-schnell",
			"Flux Realism": "flux-realism",
			"Flux Cablyai": "flux-cablyai",
			"Flux Anime": "flux-anime",
			"Flux 3D": "flux-3d",
			"Flux Disney": "flux-disney",
			"Flux Pixel": "flux-pixel",
			"Flux 4o": "flux-4o",
			"Playground v2.5": "playground-v2.5"
		}
	)
) -> None:
	await interaction.response.defer(ephemeral=False)

	try:
		response: object = await client.images.generate(
			model=modelo,
			prompt=prompt,
			response_format="url"
		)
	except HTTPException  as e:
		if e.status == 400 and e.code == 20009:
			await interaction.followup.send("Erro: O conteúdo gerado foi considerado explícito e não pode ser enviado.")
			return
		else:
			await interaction.followup.send(f"Ocorreu um erro misterioso: {str(e)}")

	if len(response.data) > 0:
		image_url: str = response.data[0].url
		async with aiohttp.ClientSession() as session:
			async with session.get(image_url) as resp:
				if resp.status == 200:
					image_bytes: Any = await resp.read()
					image_file: io.BytesIO = io.BytesIO(image_bytes)
					image_file.seek(0)
					await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**\nPrompt fornecido: `{prompt}`", file=nextcord.File(image_file, filename="imagem.png"))
				else:
					await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**\nPrompt fornecido: `{prompt}`\n[Baixar imagem!]({image_url})")
	else:
		await interaction.followup.send(f"Erro ao gerar a imagem `{prompt}`.")

def run_flask_app() -> None:
	app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
	threading.Thread(target=run_flask_app).start()
	bot.run(TOKEN)