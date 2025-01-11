from config import bot
from utils.historico import system_context, rp_modelo
from utils.rp.sys_context import create_system_context
from structures.text_models import TEXT_MODELS, DEFAULT_RP_MODEL

@bot.command(name="refreshsvctx")
async def _refrescar_contexto_servidor(ctx) -> None:
	global system_context
	if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
		system_context = await create_system_context(ctx.message.guild)
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")

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