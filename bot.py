import os
import json
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated, ChatJoinRequest
from pyrogram.errors import FloodWait

from vars import B_TOKEN, API, API_HASH, BOT_USERNAME, ownerid

# Constants
LOGO_URL = "https://ibb.co/RGFQYDby"  # Replace with your actual image URL
USER_DATA_FILE = "users.json"
GROUP_DATA_FILE = "groups.json"

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the bot
thanos = Client(
    "thanos_bot",
    bot_token=B_TOKEN,
    api_id=API,
    api_hash=API_HASH
)

# JSON storage functions
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_groups():
    try:
        with open(GROUP_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_groups(groups):
    with open(GROUP_DATA_FILE, "w") as f:
        json.dump(groups, f, indent=4)

async def add_user(user_id):
    users = load_users()
    if str(user_id) not in users:
        users.append(str(user_id))
        save_users(users)

async def add_group(group_id):
    groups = load_groups()
    if str(group_id) not in groups:
        groups.append(str(group_id))
        save_groups(groups)

# Handlers
@thanos.on_message(filters.private & filters.command(["start"]))
async def start(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        await add_user(user_id)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
        ])

        await client.send_photo(
            chat_id=message.chat.id,
            photo=LOGO_URL,
            caption="**HELLO...⚡\n\nI am an advanced Telegram auto-request accept bot.**",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Start error: {e}")
        await message.reply_text("❌ An error occurred while processing your request.")

@thanos.on_chat_member_updated(filters.group)
async def handle_chat_update(client: Client, update: ChatMemberUpdated):
    try:
        chat = update.chat
        user = update.new_chat_member.user if update.new_chat_member else update.old_chat_member.user
        
        if update.new_chat_member and update.new_chat_member.status == "member":
            await add_group(chat.id)
            await client.send_message(
                chat.id,
                f"👋 Welcome {user.mention} to {chat.title}!"
            )
        elif update.old_chat_member and update.old_chat_member.status == "left":
            await client.send_message(
                chat.id,
                f"😢 Goodbye {user.mention}, we'll miss you!"
            )
            await client.send_photo(
                user.id,
                photo=LOGO_URL,
                caption="⚠️ Sorry for any inconvenience\n👉 Contact support: @Tech_apex"
            )
    except Exception as e:
        logger.error(f"Chat update error: {e}")

@thanos.on_chat_join_request()
async def approve_request(client: Client, request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        await client.send_photo(
            request.from_user.id,
            photo=LOGO_URL,
            caption=(
                "🔥 Earn daily with our proven strategies!\n\n"
                "✅ Follow our predictions for 10X returns\n"
                "💰 High balance = High profits\n\n"
                "Join our official channel:\n"
                "https://t.me/+0t4_pyyJ0E9kNzll\n\n"
                "Register here: https://www.in444.in/#/register?invitationCode=128664713143"
            )
        )
    except Exception as e:
        logger.error(f"Join request error: {e}")

@thanos.on_message(filters.command("stats") & filters.user(ownerid))
async def show_stats(client: Client, message: Message):
    users = load_users()
    groups = load_groups()
    await message.reply_text(
        f"📊 Bot Statistics:\n\n"
        f"• Users: {len(users)}\n"
        f"• Groups: {len(groups)}\n"
        f"• Total: {len(users) + len(groups)}"
    )

@thanos.on_message(filters.command("broadcast") & filters.user(ownerid))
async def broadcast_message(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("ℹ️ Usage: /broadcast [message] or reply to a message")

    users = load_users()
    total = len(users)
    success = 0
    
    msg = await message.reply_text(f"📨 Broadcasting to {total} users...")
    
    for user_id in users:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(int(user_id))
            else:
                await client.send_message(int(user_id), message.text.split(None, 1)[1])
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Broadcast error to {user_id}: {e}")
    
    await msg.edit_text(f"✅ Broadcast complete!\nSuccess: {success}\nFailed: {total - success}")

if __name__ == "__main__":
    # Create data files if they don't exist
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(GROUP_DATA_FILE):
        with open(GROUP_DATA_FILE, "w") as f:
            json.dump([], f)
    
    logger.info("Starting bot...")
    thanos.run()
