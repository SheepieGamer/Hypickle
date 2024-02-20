import discord
import pathlib
from dotenv import load_dotenv
import os
load_dotenv()

HYPIXEL_API = os.getenv("HYPIXEL")
POLSU_API = os.getenv("POLSU")
TOKEN = os.getenv("BOT_TOKEN")
INTENTS = discord.Intents.all()

PREFIX = "h!"

BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"
