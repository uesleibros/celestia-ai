import g4f
import requests
from g4f.client import Client

# Initialize the GPT client with the desired provider and api key
client = Client()

image = requests.get("https://media.discordapp.net/attachments/1203753376140099595/1325502042826997831/imagem.png?ex=677c0579&is=677ab3f9&hm=8340569743d76251de3b07fabdadcec8e0dbbd05b639b91e447f05bd55f453f1&=&format=webp&quality=lossless&width=403&height=403", stream=True).raw
# Or: image = open("docs/images/cat.jpeg", "rb")

response = client.chat.completions.create(
    model="llama-3.1-8b",
    messages=[
        {
            "role": "user",
            "content": "O que você vê nessa imagem? fale em portugues"
        }
    ],
    provider=g4f.Provider.Blackbox,
    image=image
    # Add any other necessary parameters
)

print(response.choices[0].message.content)