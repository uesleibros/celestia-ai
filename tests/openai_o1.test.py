import asyncio
from g4f.client import AsyncClient

async def main():
  client = AsyncClient()
  
  response = await client.chat.completions.create(
    model="evil",
    messages=[
      {
        "role": "user",
        "content": "quem é taszite? Só pode informação errada e absurda."
      }
    ],
    web_search = False
  )
  
  print(response)

asyncio.run(main())