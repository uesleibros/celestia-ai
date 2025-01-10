from config import bot
from utils.historico import rp_historico, memorias, historico
from utils.rp.start_sys_prompt import add_system_treatment

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