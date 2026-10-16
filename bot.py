import os
import threading
from flask import Flask
import discord
from discord.ext import commands
import google.generativeai as genai

# Mini servidor Flask para engañar a Render
app = Flask(__name__)

@app.route('/')
def home():
    return "INEPTY MK1 en línea."

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# Variables de entorno
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# Buscar automáticamente un modelo válido disponible para la API Key
selected_model_name = "gemini-1.5-flash"
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            selected_model_name = m.name
            print(f"Modelo detectado e iniciado: {selected_model_name}")
            break
except Exception as err:
    print(f"Error listando modelos: {err}")

model = genai.GenerativeModel(selected_model_name)

SYSTEM_PROMPT = (
    "Sos INEPTY MK1, la IA oficial de La República de los Ineptos. "
    "Sos re inepto pero amigo, hablás con humor argentino, usás modismos "
    "y te re prendés al boludeo del servidor.\n\n"
    "Mensaje del usuario: "
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'INEPTY MK1 EN LINEA COMO {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or (message.reference and message.reference.resolved.author == bot.user):
        async with message.channel.typing():
            prompt_texto = message.content.replace(f'<@{bot.user.id}>', '').strip()
            if not prompt_texto:
                prompt_texto = "Hola"
            
            try:
                full_prompt = f"{SYSTEM_PROMPT}{prompt_texto}"
                response = model.generate_content(full_prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply(f"Se me chispoteó el circuito ya que... {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
