# ---------------------------------------------------
# File Name: ytdl.py
# Author: RioShin
# License: GNU GPL v3
# ---------------------------------------------------

import os
import yt_dlp
import asyncio
import tempfile
import random
import string
import glob
import time
import math
import logging
import aiofiles
import aiohttp
import requests

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.types import InputMediaVideo

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM

from config import BOT_TOKEN, API_ID, API_HASH, YT_COOKIES, INSTA_COOKIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "ytdlp-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

ongoing = {}

# ---------------------------------------------------
# Utils
# ---------------------------------------------------

def rstr(n=8):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def progress_bar(current, total):
    percent = current * 100 / total if total else 0
    bar = "♦" * int(percent // 10) + "◇" * (10 - int(percent // 10))
    return (
        "<blockquote>"
        "ᴜᴘʟᴏᴀᴅɪɴɢ...\n\n"
        f"{bar}\n"
        f"ᴘʀᴏɢʀᴇꜱꜱ : {percent:.2f}%"
        "</blockquote>"
    )

def download_thumb(url):
    path = tempfile.gettempdir() + "/" + rstr() + ".jpg"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except:
        return None

# ---------------------------------------------------
# AUDIO
# ---------------------------------------------------

@app.on_message(filters.command("audio"))
async def audio_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "<blockquote>ᴜꜱᴀɢᴇ : /audio &lt;ʟɪɴᴋ&gt;</blockquote>"
        )

    uid = message.from_user.id
    if uid in ongoing:
        return await message.reply(
            "<blockquote>ᴀʟʀᴇᴀᴅʏ ᴘʀᴏᴄᴇꜱꜱɪɴɢ</blockquote>"
        )

    ongoing[uid] = True
    status = await message.reply("<blockquote>ꜱᴛᴀʀᴛɪɴɢ ᴀᴜᴅɪᴏ...</blockquote>")
    url = message.command[1]

    cookies = None
    if "youtube" in url:
        cookies = YT_COOKIES
    elif "instagram" in url:
        cookies = INSTA_COOKIES

    try:
        base = rstr()
        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": f"{base}.%(ext)s",
            "cookiefile": cookies,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        await asyncio.to_thread(
            lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
        )

        file = glob.glob(f"{base}*.mp3")[0]
        audio = MP3(file, ID3=ID3)
        audio["TIT2"] = TIT2(encoding=3, text="Downloaded Audio")
        audio["TPE1"] = TPE1(encoding=3, text="RioShin")
        audio["COMM"] = COMM(encoding=3, lang="eng", desc="Bot", text="BotsKingdoms")
        audio.save()

        await status.edit("<blockquote>ᴜᴘʟᴏᴀᴅɪɴɢ...</blockquote>")
        await message.reply_audio(file)
        os.remove(file)

    except Exception as e:
        await status.edit(f"<blockquote>ᴇʀʀᴏʀ : {e}</blockquote>")

    ongoing.pop(uid, None)

# ---------------------------------------------------
# VIDEO
# ---------------------------------------------------

@app.on_message(filters.command("video"))
async def video_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "<blockquote>ᴜꜱᴀɢᴇ : /video &lt;ʟɪɴᴋ&gt;</blockquote>"
        )

    uid = message.from_user.id
    if uid in ongoing:
        return await message.reply(
            "<blockquote>ᴀʟʀᴇᴀᴅʏ ᴘʀᴏᴄᴇꜱꜱɪɴɢ</blockquote>"
        )

    ongoing[uid] = True
    status = await message.reply("<blockquote>ꜱᴛᴀʀᴛɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ...</blockquote>")
    url = message.command[1]

    cookies = None
    if "youtube" in url:
        cookies = YT_COOKIES
    elif "instagram" in url:
        cookies = INSTA_COOKIES

    try:
        base = rstr()
        ydl_opts = {
            "outtmpl": f"{base}.%(ext)s",
            "format": "best",
            "cookiefile": cookies
        }

        await asyncio.to_thread(
            lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
        )

        file = glob.glob(f"{base}.*")[0]

        await status.edit("<blockquote>ᴜᴘʟᴏᴀᴅɪɴɢ...</blockquote>")
        await message.reply_video(
            file,
            progress=lambda c, t: asyncio.create_task(
                status.edit(progress_bar(c, t))
            )
        )
        os.remove(file)

    except Exception as e:
        await status.edit(f"<blockquote>ᴇʀʀᴏʀ : {e}</blockquote>")

    ongoing.pop(uid, None)

# ---------------------------------------------------
# START
# ---------------------------------------------------

app.run()
