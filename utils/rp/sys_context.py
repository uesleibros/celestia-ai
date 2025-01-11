import json
import nextcord
from typing import List, Dict, Union

async def create_system_context(guild: nextcord.Guild) -> str:
  categories: List[Dict[str, str]] = []
  uncategorized_channels: List[Dict[str, str]] = []

  for channel in guild.channels:
    if isinstance(channel, nextcord.CategoryChannel):
      categories.append({
        "id": channel.id,
        "name": channel.name,
        "type": "category",
        "channels": [
          {"id": c.id, "name": c.name, "type": str(c.type)} for c in channel.channels
        ]
      })
    elif channel.category is None:
      uncategorized_channels.append({
        "id": channel.id,
        "name": channel.name,
        "type": str(channel.type)
      })

  emojis: List[Dict[str, str]] = [{"name": emoji.name, "id": emoji.id, "mention": str(emoji)} for emoji in guild.emojis]
  created_at: List[Dict[str, str]] = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")

  server_info: Dict[str, Union[str, List[Dict[str, str]]]] = {
    "server_name": guild.name,
    "server_id": guild.id,
    "server_icon_url": guild.icon.url if guild.icon else None,
    "category_count": len(categories),
    "channel_count": len(guild.channels),
    "server_creation_date": created_at,
    "categories": categories,
    "channels_outside_categories": uncategorized_channels,
    "emojis": emojis[20:]
  }

  return json.dumps(server_info, indent=2)