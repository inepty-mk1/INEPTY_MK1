import discord
from discord.ext import commands
import google.generativeai as genai

# Configuración de las claves
DISCORD_TOKEN = "MTU2MDQzNTAwNzQ2ODczNjU1Mg.GSlv23.GDqWHrq8IU1J0CvPPRI-U7oLlyjjD90WryKfqI"
GEMINI_API_KEY = "AQ.Ab8RN6Kisd49NyT4YmxxxkvfwU_A_z7-UI0Vv_Mn38p9CEPyGQ"

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

    # Responder si lo mencionan o le responden un mensaje
    if bot.user.mentioned_in(message) or (message.reference and message.reference.resolved.author == bot.user):
        async with message.channel.typing():
            prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
            if not prompt:
                prompt = "Hola"
            
            try:
                response = model.generate_content(prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply("Se me chispoteó el circuito, probá de nuevo.")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
