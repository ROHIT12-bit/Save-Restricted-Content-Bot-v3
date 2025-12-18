# Copyright (c) 2025 RioShin : https://github.com/Rioshin2025.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from datetime import datetime, timedelta
from shared_client import client as bot_client
from telethon import events
from utils.func import (
    get_display_name,
    is_private_chat,
    premium_users_collection,
    is_premium_user
)
from config import OWNER_ID
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('teamspy')


# ------------------- ADD PREMIUM -------------------
@bot_client.on(events.NewMessage(pattern=r'^/add_premium(?:\s+|$)'))
async def add_premium_handler(event):
    if not await is_private_chat(event):
        return
    if event.sender_id not in OWNER_ID:
        return

    args = event.text.split()
    if len(args) != 2:
        await event.respond(
            "Usage:\n/add_premium <user_id>\nExample: /add_premium 123456789"
        )
        return

    try:
        target_user_id = int(args[1])
    except ValueError:
        await event.respond("❌ User ID must be a number")
        return

    now = datetime.utcnow()
    expiry = now + timedelta(days=365)  # default 1 year, adjust if needed

    await premium_users_collection.update_one(
        {"user_id": target_user_id},
        {
            "$set": {
                "user_id": target_user_id,
                "subscription_start": now,
                "subscription_end": expiry,
                "expireAt": expiry
            }
        },
        upsert=True
    )

    expiry_ist = expiry + timedelta(hours=5, minutes=30)
    formatted_expiry = expiry_ist.strftime("%d-%b-%Y %I:%M:%S %p")

    await event.respond(
        f"✅ Premium added for `{target_user_id}`\n"
        f"⏳ Valid till: {formatted_expiry} (IST)"
    )

    try:
        await bot_client.send_message(
            target_user_id,
            f"🌟 Premium activated!\nValid till: {formatted_expiry} (IST)"
        )
    except Exception:
        pass


# ------------------- LIST PREMIUM -------------------
@bot_client.on(events.NewMessage(pattern=r'^/premium_list$'))
async def premium_list_handler(event):
    if not await is_private_chat(event):
        return
    if event.sender_id not in OWNER_ID:
        return

    users = premium_users_collection.find()
    text = "🌟 **Premium Users List**\n\n"
    count = 0

    async for user in users:
        count += 1
        uid = user["user_id"]
        expiry = user.get("subscription_end")
        if expiry:
            expiry_ist = expiry + timedelta(hours=5, minutes=30)
            expiry_str = expiry_ist.strftime("%d-%b-%Y")
        else:
            expiry_str = "Unknown"
        text += f"{count}. `{uid}` — till {expiry_str}\n"

    if count == 0:
        text = "⚠️ No premium users found."

    await event.respond(text)


# ------------------- REMOVE PREMIUM -------------------
@bot_client.on(events.NewMessage(pattern=r'^/remove_premium(?:\s+|$)'))
async def remove_premium_handler(event):
    if not await is_private_chat(event):
        return
    if event.sender_id not in OWNER_ID:
        await event.respond("❌ Not authorized")
        return

    args = event.text.split()
    if len(args) != 2:
        await event.respond(
            "Usage:\n/remove_premium <user_id>\nExample: /remove_premium 123456789"
        )
        return

    try:
        target_user_id = int(args[1])
    except ValueError:
        await event.respond("❌ Invalid user ID")
        return

    if not await is_premium_user(target_user_id):
        await event.respond(
            f"❌ User `{target_user_id}` does not have a premium subscription."
        )
        return

    try:
        result = await premium_users_collection.delete_one(
            {"user_id": target_user_id}
        )
        if result.deleted_count == 0:
            await event.respond("❌ Failed to remove premium (not found).")
            return

        target_name = "Unknown"
        try:
            entity = await bot_client.get_entity(target_user_id)
            target_name = get_display_name(entity)
        except Exception:
            pass

        await event.respond(
            f"✅ Premium successfully removed from {target_name} (`{target_user_id}`)"
        )

        try:
            await bot_client.send_message(
                target_user_id,
                "⚠️ Your premium subscription has been removed by the admin."
            )
        except Exception:
            pass

    except Exception as e:
        logger.error(f"Error removing premium: {e}")
        await event.respond("❌ Error while removing premium.")
