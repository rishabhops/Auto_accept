import os
import json
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated, ChatJoinRequest
from pyrogram.errors import FloodWait

from vars import B_TOKEN, API, API_HASH, BOT_USERNAME, ownerid

# Constants
LOGO_URL = "https://graph.org/file/98a15d8ecbd89eb30f7aa.jpg"
USER_DATA_FILE = "user_data.json"
GROUP_DATA_FILE = "group_data.json"
SERVED_USERS_FILE = "served_users.json"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
thanos = Client(
    "bot_started",
    bot_token=B_TOKEN,
    api_id=API,
    api_hash=API_HASH
)

# Helper functions for local database
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def add_to_data(data_list, new_entry, file_path):
    if new_entry not in data_list:
        data_list.append(new_entry)
        save_data(data_list, file_path)

# Load initial data
user_data = load_data(USER_DATA_FILE)
group_data = load_data(GROUP_DATA_FILE)
served_users = load_data(SERVED_USERS_FILE)

# Functions to replace MongoDB operations
async def add_served_user(user_id):
    """Add a user to the served users list"""
    user_id = str(user_id)  # Convert to string for JSON compatibility
    user_data = {"user_id": user_id}
    
    # Check if user already exists in served_users
    if not any(user["user_id"] == user_id for user in served_users):
        served_users.append(user_data)
        save_data(served_users, SERVED_USERS_FILE)
        logger.info(f"Added user {user_id} to served users.")

async def get_served_users():
    """Get all served users"""
    return served_users

# Handlers
@thanos.on_message(filters.private & filters.command(["start"]))
async def start(client: Client, message: Message):
    try:
        await add_served_user(message.from_user.id)
        logger.info(f"Added user {message.from_user.id} to the database.")

        button = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
        ]

        await client.send_photo(
            chat_id=message.chat.id,
            photo=LOGO_URL,
            caption="**HELLO...⚡\n\ni am an advanced telegram auto request accept bot.**",
            reply_markup=InlineKeyboardMarkup(button)
        )

        logger.info(f"Sent start message to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.reply_text(f"An error occurred: {e}")

@thanos.on_chat_member_updated(filters.group)
async def welcome_goodbye(client: Client, message: ChatMemberUpdated):
    try:
        new_chat_member = message.new_chat_member
        old_chat_member = message.old_chat_member
        chat = message.chat

        if new_chat_member:
            if new_chat_member.status == "member":
                add_to_data(group_data, chat.id, GROUP_DATA_FILE)
                user = new_chat_member.user
                logger.info(f"{user.first_name} joined {chat.title}")
                await client.send_message(
                    chat_id=chat.id,
                    text=f"Hello {user.mention}, welcome to {chat.title}!"
                )
        elif old_chat_member:
            if old_chat_member.status == "left":
                user = old_chat_member.user
                logger.info(f"{user.first_name} left {chat.title}")
                await client.send_message(
                    chat_id=chat.id,
                    text=f"Goodbye {user.mention}, we will miss you in {chat.title}!"
                )

                personal_goodbye_message = (
                    "⚠️ Sorry for the inconvenience caused\n"
                    "🚨 You Can Request any Anime here\n"
                    "👉 https://t.me/SonuBhaiyaBot\n"
                    "🛎️ Koi bhi Help ke liye msg here ☝️"
                )

                await client.send_photo(
                    chat_id=user.id,
                    photo=LOGO_URL,
                    caption=personal_goodbye_message
                )
    except Exception as e:
        logger.error(f"Error in welcome_goodbye handler: {e}")

@thanos.on_chat_join_request()
async def autoapprove(client: Client, message: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        logger.info(f"Approved join request for {message.from_user.first_name} in {message.chat.title}")

        # Add user to served users
        await add_served_user(message.from_user.id)
        
        # Add user to user data if not already there
        user_id = message.from_user.id
        if user_id not in user_data:
            add_to_data(user_data, user_id, USER_DATA_FILE)

        personal_message = (
            f"💋𝙅𝙤𝙞𝙣 𝙁𝙤𝙧 𝙇𝙖𝙩𝙚𝙨𝙩 𝘾𝙤𝙡𝙡𝙚𝙘𝙩𝙞𝙤𝙣💋\n\n"
            "• https://discord.com/invite/5ACnAvC2et\n"
            "• https://discord.com/invite/5ACnAvC2et\n"
            "• https://discord.com/invite/5ACnAvC2et\n"
            "• https://discord.com/invite/5ACnAvC2et\n\n"
            "🎬Click Here to learn how to login in Discord\n\n"
            "@HowToUse_Discord\n"
            "@HowToUse_Discord\n\n"
            "🎬डिस्कॉर्ड में लॉगइन करने का तरीका जानने के लिए यहां क्लिक करें"
        )

        await client.send_photo(
            chat_id=message.from_user.id,
            photo=LOGO_URL,
            caption=personal_message
        )
    except Exception as e:
        logger.error(f"Error in autoapprove handler: {e}")

@thanos.on_message(filters.command("stats") & filters.user(ownerid))
async def stats(client: Client, message: Message):
    users = len(await get_served_users())
    await message.reply_text(
        f"ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {client.me.mention} :\n\n➻ ᴜsᴇʀs : {users}\n"
    )

@thanos.on_message(filters.command("broadcast") & filters.user(ownerid))
async def broadcast(cli: Client, message: Message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "ᴇxᴀᴍᴘʟᴇ :\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]"
            )
        query = message.text.split(None, 1)[1]

    susr = 0
    served_user_list = await get_served_users()
    
    for user in served_user_list:
        user_id = int(user["user_id"])
        try:
            m = (
                await cli.copy_message(chat_id=user_id, from_chat_id=y, message_id=x)
                if message.reply_to_message
                else await cli.send_message(user_id, text=query)
            )
            susr += 1
            await asyncio.sleep(0.2)
        except FloodWait as e:
            flood_time = int(e.value)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception as e:
            logger.error(f"Error sending broadcast to {user_id}: {e}")
            continue

    try:
        await message.reply_text(f"ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {susr} ᴜsᴇʀs.")
    except:
        pass

if __name__ == "__main__":
    thanos.run()
