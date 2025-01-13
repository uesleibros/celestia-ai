from config import bot
from utils.historico import rp_modelo
from structures.text_models import TEXT_MODELS, DEFAULT_RP_MODEL

@bot.command(name="refreshmod")
async def _refrescar_modelo(ctx) -> None:
	global rp_modelo
	if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
		rp_modelo = DEFAULT_RP_MODEL
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")

@bot.command(name="chgmod")
async def _mudar_modelo(ctx, modelo_valor: str) -> None:
	global rp_modelo
	if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
		if modelo_valor in TEXT_MODELS.values():
			rp_modelo = modelo_valor
			await ctx.message.add_reaction("✅")
		else:
			await ctx.message.add_reaction("❌")
	else:
		await ctx.message.add_reaction("❌")