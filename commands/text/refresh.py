from config import bot
from utils.historico import system_context
from utils.rp.sys_context import create_system_context

@bot.command(name="refreshsvctx")
async def _refrescar_contexto_servidor(ctx) -> None:
	global system_context
	if ctx.author.id == 764259870563631114 or ctx.author.guild_permissions.administrator:
		system_context = await create_system_context(ctx.message.guild)
		await ctx.message.add_reaction("✅")
	else:
		await ctx.message.add_reaction("❌")