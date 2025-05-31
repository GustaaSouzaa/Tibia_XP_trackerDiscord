import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from core.api import get_character_info_with_exp  # sua função importada do api.py

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}!")

@bot.command(name="character")
async def character(ctx, *, name: str = None):
    if not name:
        await ctx.send("Por favor, informe o nome do personagem. Uso: `!character <nome>`")
        return

    await ctx.send(f"Buscando dados do personagem {name}...")

    data = get_character_info_with_exp(name)

    if "error" in data:
        await ctx.send(f"Erro: {data['error']}")
        return

    exp = data.get("experience")
    exp_str = str(exp) if exp is not None else "N/A"

    deaths = data.get("deaths", 0)
    if isinstance(deaths, list):
        deaths = len(deaths)

    msg = (
        f"**Dados de {data['name']}:**\n"
        f"Nível: {data['level']}\n"
        f"Vocação: {data['vocation']}\n"
        f"Mundo: {data['world']}\n"
        f"Experiência: {exp_str}\n"
        f"Online: {data.get('online', False)}\n"
        f"Último login: {data.get('last_login', 'N/A')}\n"
        f"Mortes: {deaths}"
    )
    await ctx.send(msg)

bot.run(TOKEN)
