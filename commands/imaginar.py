from nextcord import Interaction, SlashOption, File
from config import bot, client
from structures.image_models import IMAGE_MODELS
import aiohttp
import io

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
		choices=IMAGE_MODELS,
		default="midjourney"
	),
	fantasma: bool = SlashOption(
		name="fantasma",
		description="Ao ativar essa opção, só você poderá ver esse comando sendo executado.",
		required=False,
		default=False
	)
) -> None:
	await interaction.response.defer(ephemeral=fantasma)

	try:
		print(f"{interaction.user} — gerou uma imagem com o modelo {modelo} usando o prompt: {prompt}")
		response: object = await client.images.generate(
			model=modelo,
			prompt=prompt,
			response_format="url"
		)
		
		if len(response.data) > 0:
			image_url: str = response.data[0].url
			async with aiohttp.ClientSession() as session:
				async with session.get(image_url) as resp:
					if resp.status == 200:
						image_bytes: Any = await resp.read()
						image_file: io.BytesIO = io.BytesIO(image_bytes)
						image_file.seek(0)
						await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**\nPrompt fornecido: `{prompt}`", file=File(image_file, filename="imagem.png"))
					else:
						await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**\nPrompt fornecido: `{prompt}`\n[Baixar imagem!]({image_url})")
		else:
			await interaction.followup.send(f"Erro ao gerar a imagem `{prompt}`.")
	except Exception  as e:
		await interaction.followup.send(f"Ocorreu um erro misterioso: {str(e)}")
		return