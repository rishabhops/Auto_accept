#.this version have a ability to send pictures in dms
import os
import json
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated, ChatJoinRequest
from pyrogram.errors import FloodWait

from vars import B_TOKEN, API, API_HASH, BOT_USERNAME, DB_URI, ownerid
from rishabh.users_db import get_served_users, add_served_user
from async_mongo import AsyncClient

# Constants
LOGO_URL = "https://graph.org/file/98a15d8ecbd89eb30f7aa.jpg"
USER_DATA_FILE = "user_data.json"
GROUP_DATA_FILE = "group_data.json"

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

# Connect to MongoDB
try:
    mongo = AsyncClient(DB_URI)
    db = mongo["Assistant"]
    logger.info("Connected to your Mongo Database.")
except Exception as e:
    logger.error(f"Failed to connect to your Mongo Database: {e}")
    exit(1)

usersdb = db["users"]

# Helper functions
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

user_data = load_data(USER_DATA_FILE)
group_data = load_data(GROUP_DATA_FILE)

def add_to_data(data_list, new_entry, file_path):
    if new_entry not in data_list:
        data_list.append(new_entry)
        save_data(data_list, file_path)

# Handlers
@thanos.on_message(filters.private & filters.command(["start"]))
async def start(client: Client, message: Message):
    try:
        await add_served_user(message.from_user.id)
        logger.info(f"Added user {message.from_user.id} to the database.")

        button = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
        ]

        # Test if the bot can send a simple text message
        # await client.send_message(
        #    chat_id=message.chat.id,
        #    text="Bot is working! This is a test message."
        # )

        # Uncomment this part after confirming the bot can send messages
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
async def welcome_goodbye(client: thanos, message: ChatMemberUpdated):
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
                    "👉 https://t.me/Tech_apex\n"
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
async def autoapprove(client: thanos, message: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        logger.info(f"Approved join request for {message.from_user.first_name} in {message.chat.title}")

        personal_message = (
            f"ऐसे ही नहीं तुम्हारा भाई DAILY के 100k से 150K तक कमाता है 🔥 Live देख लो ख़तरनाक earning होती है ✔️\n\n"
            "✅Total Din के Prediction Follow\nEarning 10X…. (DIRECT)📈\n\n"
            "🤑 High Balance Huge Profit जीतना ज़्यादा बैलेंस हौगा उतना ज़्यादा प्रोफ़िट हौगा\n\n"
            "Join Official Sureshot Channel  ✅\n"
            "https://t.me/+0t4_pyyJ0E9kNzll\n"
            "https://t.me/+0t4_pyyJ0E9kNzll\n\n"
            "Registered Link 👉 https://www.in444.in/#/register?invitationCode=128664713143"
        )

        await client.send_photo(
            chat_id=message.from_user.id,
            photo=LOGO_URL,
            caption=personal_message
        )
    except Exception as e:
        logger.error(f"Error in autoapprove handler: {e}")

@thanos.on_message(filters.command("stats") & filters.user(ownerid))
async def stats(client: thanos, message: Message):
    users = len(await get_served_users())
    await message.reply_text(
        f"<u><b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {client.me.mention} :</b></u>\n\n➻ <b>ᴜsᴇʀs :</b> {users}\n"
    )

@thanos.on_message(filters.command("broadcast") & filters.user(ownerid))
async def broadcast(cli: thanos, message: Message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "<b>ᴇxᴀᴍᴘʟᴇ </b>:\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]"
            )
        query = message.text.split(None, 1)[1]

    susr = 0
    served_users = []
    susers = await get_served_users()
    for user in susers:
        served_users.append(int(user["user_id"]))
    for i in served_users:
        try:
            m = (
                await cli.copy_message(chat_id=i, from_chat_id=y, message_id=x)
                if message.reply_to_message
                else await cli.send_message(i, text=query)
            )
            susr += 1
            await asyncio.sleep(0.2)
        except FloodWait as e:
            flood_time = int(e.value)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except:
            continue

    try:
        await message.reply_text(f"<b>ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {susr} ᴜsᴇʀs.</b>")
    except:
        pass

if __name__ == "__main__":
    thanos.run()
                  
