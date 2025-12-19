# Copyright (c) 2025 RioShin : https://github.com/Rioshin2025.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telethon BOT
client = TelegramClient(
    "telethon_bot",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# Pyrogram BOT
app = Client(
    "pyrogram_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ❌ Userbot disabled
userbot = None

async def start_client():
    await app.start()
    logger.info("Telethon + Pyrogram bot started (NO USERBOT)")
    return client, app, None
