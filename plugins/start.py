# Copyright (c) 2025 RioShin : https://github.com/Rioshin2025.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_GROUP, OWNER_ID, FORCE_SUB

# ----------------- Start command handler -----------------
@ app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    # Inline buttons: 2 rows
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/BOTSKINGDOMS"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/BOTSKINGDOMSGROUP")
            ],
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RioShin")
            ]
        ]
    )

    # Start image and caption
    START_IMAGE = "https://i.rj1.dev/vgrAW.png"
    caption_text = """<blockquote>**👋 ʜɪ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ sᴀᴠᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ ʙᴏᴛ**</blockquote>
<blockquote>**❤️‍🔥 sᴀᴠᴇ ᴘᴏsᴛs ғʀᴏᴍ ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀɴɴᴇʟs & ɢʀᴏᴜᴘs**</blockquote>
<blockquote>**❤️‍🔥 ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ ғʀᴏᴍ sᴜᴘᴘᴏʀᴛᴇᴅ ᴘʟᴀᴛғᴏʀᴍs**</blockquote>
<blockquote>**📎 sᴇɴᴅ ᴀ ᴘᴏsᴛ ʟɪɴᴋ ᴛᴏ sᴛᴀʀᴛ**</blockquote>
<blockquote>**⚙️ ᴜsᴇ /cmd ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs**</blockquote>
<blockquote>**⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ** <a href='https://t.me/BOTSKINGDOMS'>BotsKingdoms</a></blockquote>"""

    await client.send_photo(
        chat_id=message.chat.id,
        photo=START_IMAGE,
        caption=caption_text,
        reply_markup=markup
    )

# ----------------- Subscription check -----------------
async def subscribe(app, message):
    if FORCE_SUB:
        try:
            user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
            if str(user.status) == "ChatMemberStatus.BANNED":
                await message.reply_text("You are Banned. Contact -- Team SPY")
                return 1
        except UserNotParticipant:
            link = await app.export_chat_invite_link(FORCE_SUB)
            caption = f"""**⚠️ Hᴇʏ, ᴅᴜᴅᴇ
Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ғᴇᴡ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ. Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟs ᴘʀᴏᴠɪᴅᴇᴅ ʙᴇʟᴏᴡ, ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ.. !

❗Fᴀᴄɪɴɢ ᴘʀᴏʙʟᴇᴍs, ᴅᴍ @RioShin**"""
            await message.reply_photo(
                photo="https://i.rj1.dev/vgrAW.png",
                caption=caption,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now...", url=f"{link}")]])
            )
            return 1
        except Exception as ggn:
            await message.reply_text(f"Something Went Wrong. Contact admins... with following message {ggn}")
            return 1 

# ----------------- Cmd pages -----------------
help_pages = [
    (
        """<blockquote>🤖 Bot Commands Guide — PART 1</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>👑 OWNER COMMANDS</blockquote>
<blockquote>/add &lt;user_id&gt; – Grant premium access</blockquote>
<blockquote>/rem &lt;user_id&gt; – Revoke premium access</blockquote>
<blockquote>/get – View all registered user IDs</blockquote>
<blockquote>/lock – Lock a channel from extraction</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>💎 PREMIUM / USER</blockquote>
<blockquote>/transfer &lt;user_id&gt; – Transfer premium (Resellers)</blockquote>
<blockquote>/login – Login for private channel access</blockquote>
<blockquote>/logout – Logout from bot</blockquote>
<blockquote>/myplan – View your active plan</blockquote>
<blockquote>/plan – Check premium plans</blockquote>
<blockquote>/terms – Terms &amp; conditions</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>📥 DOWNLOAD & EXTRACTION</blockquote>
<blockquote>/dl &lt;link&gt; – Download video </blockquote>
<blockquote>/adl &lt;link&gt; – Download audio </blockquote>
<blockquote>/batch – Bulk post extraction (Login required)</blockquote>
<blockquote>/cancel – Cancel ongoing process</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>⚡ by @Botskingdoms</blockquote>
"""
    ),
    (
        """<blockquote>🤖 Bot Commands Guide — PART 2</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>⚙️ SETTINGS</blockquote>
<blockquote>SETCHATID – Upload directly to channel / group / DM (Use -100&lt;chat_id&gt;)</blockquote>
<blockquote>SETRENAME – Add custom rename tag or channel username</blockquote>
<blockquote>CAPTION – Set custom caption</blockquote>
<blockquote>REPLACEWORDS – Replace removed words</blockquote>
<blockquote>RESET – Restore default settings</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>✨ Extra Features</blockquote>
<blockquote>Custom Thumbnail</blockquote>
<blockquote>PDF Watermark</blockquote>
<blockquote>Video Watermark</blockquote>
<blockquote>Session-based Login</blockquote>
<blockquote>━━━━━━━━━━━━━━━━━━</blockquote>
<blockquote>⚡ Powered by @BotsKingdoms</blockquote>
"""
    )
]
# ----------------- Help navigation -----------------
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
     
    prev_button = InlineKeyboardButton("ᴘʀᴇᴠɪᴏᴜs", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("ɴᴇxᴛ", callback_data=f"help_next_{page_number}")
 
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
    keyboard = InlineKeyboardMarkup([buttons])
 
    await message.delete()
 
    await message.reply(help_pages[page_number], reply_markup=keyboard)
 
@app.on_message(filters.command("cmd"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
     
    await send_or_edit_help_page(client, message, 0)
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    await send_or_edit_help_page(client, callback_query.message, page_number)
    await callback_query.answer()

# -----------------  Plan commands -----------------
@app.on_message(filters.command("plans") & filters.private)
async def plan(client, message):
    plan_text = """ 💖 Premium Benefits
~ High-speed uploads.
~ Fetch content from private/private channel.
~ Fetch content from private/public group.
~ Join any chat by sending invite link.
~ Supports Batch system for multiple files

💵 Plans & Prices (No Bargains)
~ 7 Days (1$/₹50)
~ 30 Days (2$/₹100)
~ Quaterly (3$/₹150)  
~ Half-Year (4$/₹300)  
~ Full-Year (5$/₹600)  

✅ Click the button below for your subscription!"""
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/RioShin")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)

