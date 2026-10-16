import os
import threading
from flask import Flask
import discord
from discord.ext import commands
import google.generativeai as genai

# Mini servidor Flask para engañar el escaneo de puertos de Render
app = Flask(__name__)

@app.route('/')
def home():
    return "INEPTY MK1 en línea y operando."

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Inicia Flask en un hilo secundario
threading.Thread(target=run_flask, daemon=True).start()

# Configuración de las claves desde las variables de entorno de Render
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Sos INEPTY MK1, la IA oficial de La República de los Ineptos. Sos re inepto pero amigo, hablás con humor argentino, usás modismos y te re prendés al boludeo del servidor."
)

# Configurar Discord Bot
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
            prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
            if not prompt:
                prompt = "Hola"
            
            try:
                response = model.generate_content(prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply(f"Se me chispoteó el circuito ya que... {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
