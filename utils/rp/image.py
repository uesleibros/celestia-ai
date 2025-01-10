import g4f
from config import client

async def analyze_image(prompt: str, image: bytes) -> str:
  try:
    response: object = await client.chat.completions.create(
      model="llama-3.1-70b",
      messages=[{"role": "user", "content": prompt + ". Responda em português com todos os detalhes da imagem, bem detalhado mesmo"}],
      provider=g4f.Provider.Blackbox,
      image=image
    )

    if len(response.choices) > 0:
      return response.choices[0].message.content
    return None
  except Exception as e:
    return None 