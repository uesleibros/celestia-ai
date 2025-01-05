from nextcord import Interaction, SlashOption, File, Attachment
from config import bot, client
from structures.image_models import IMAGE_MODELS
import aiohttp
import io

@bot.slash_command(
	name="criar-variacao",
	description="Gere a imagem dos seus sonhos ☺.",
)
async def criar_variacao(
	interaction: Interaction,
	referencia: Attachment = SlashOption(
		name="referencia",
		description="Imagem que você quer que eu use como base pra gerar uma variante.",
		required=True
	),
	modelo: str = SlashOption(
		name="modelo",
		description="Escolha o modelo de IA.",
		choices=IMAGE_MODELS,
		default="midjourney"
	)
) -> None:
	await interaction.response.defer(ephemeral=False)

	try:
		if referencia:
			image_bytes = await referencia.read()
		response: object = await client.images.create_variation(
			model=modelo,
			image=image_bytes,
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
						await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**", file=File(image_file, filename="imagem.png"))
					else:
						await interaction.followup.send(f"{interaction.user.mention} Modelo escolhido: **{modelo}**\n[Baixar imagem!]({image_url})")
		else:
			await interaction.followup.send(f"Erro ao gerar a imagem `{prompt}`.")
	except Exception  as e:
		await interaction.followup.send(f"Ocorreu um erro misterioso: {str(e)}")
		return