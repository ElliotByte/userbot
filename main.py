from pyrogram import Client, filters
import random
import asyncio
import time
import os
import logging
from pyrogram.errors import FloodWait, RPCError
from telethon.sync import TelegramClient, functions
import tgcrypto 
from telethon import TelegramClient
from telethon.sessions import StringSession
import time
import logging
import sys
from pyrogram.types import Message



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api_id = 
api_hash = ""
app = Client("my_account", api_id=api_id, api_hash=api_hash)
OWNER_ID =      


# type - beautiful typing of text
@app.on_message(filters.command("type", prefixes=".") & filters.user(OWNER_ID))
async def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" 
    typing_symbol = "▒"
    while tbp != orig_text:
        await msg.edit(tbp + typing_symbol)
        await asyncio.sleep(0.05)
        tbp = tbp + text[0]
        text = text[1:]
        await msg.edit(tbp)
        await asyncio.sleep(0.05)


#id - shows the IDs of other accounts. Only works if you reply to a user's message
@app.on_message(filters.command("id", prefixes=".") & filters.user(OWNER_ID))
async def send_user_id(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        await message.reply_text(f"{user.id}")
    else:
        text = message.text.replace(".id @", "")
        user = await app.get_users(text)
        await message.reply_text(f"{user.id}")


# calculator
@app.on_message(filters.command("count", prefixes=".") & filters.user(OWNER_ID))
async def count(client, message):
    comand = message.text.replace(".count ", "")
    try:
        answer = eval(comand)
        await message.reply_text(f"{comand} = {answer}")
    except Exception as e:
        await message.reply_text(f"Ошибка: {e}")


#Be careful. In large chats, you can get a temporary telegram account mute
@app.on_message(filters.command("spam", prefixes=".") & filters.user(OWNER_ID))
async def spam_messages(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply_text("# Usage:.spam quantity text")
# e.g. - .spam 10 hello
      return
    count = args[1]
    text = args[2]
    for _ in range(int(count)):
        await asyncio.sleep(0.1)
        await message.reply_text(text)

# Parsing of all chat participants. In large chats, you can get a temporary telegram account mute
@app.on_message(filters.command("парсинг", prefixes=".") & filters.user(OWNER_ID))
async def parse_users(client, message):
    chat_id = message.chat.id
    users_info = []
    owner_id = OWNER_ID

    async for member in app.get_chat_members(chat_id):
        user = member.user
        if user.id == owner_id:
            continue

        phone_number = f", Number: {user.phone_number}" if user.phone_number else ""
        user_info = f"@{user.username if user.username else 'None'} (ID: {user.id}, Name: {user.first_name}{phone_number})"
        users_info.append(user_info)

    result_message = "\n".join(users_info)
    await message.reply_text(result_message)




def split_message(text, max_length):
    if len(text) <= max_length:
        return [text]

    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind('\n')
        if split_index == -1:
            split_index = text[:max_length].rfind(' ')
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index].strip())
        text = text[split_index:].strip()

    if text:
        parts.append(text)

    return parts




#Complete cleaning of all your chat messages. If there are a lot of messages (>1000), you will have to wait for a while. Works in both private and public chats
@app.on_message(filters.command("clear", prefixes=".") & filters.user(OWNER_ID))
async def delete_my_messages(client, message):
    chat_id = message.chat.id
    
    await message.delete()  
    
    async for msg in client.get_chat_history(chat_id):
        if msg.from_user and msg.from_user.id == OWNER_ID:
            try:
                await client.delete_messages(chat_id, msg.id)  
            except Exception as e:
                print(f"Message Could Not Be Deleted {msg.id}: {e}")


# User hate. Write in [ ] all bad messages that will automatically respond to the person you have chosen. 
# Example of use:.hate 384849302 (384849302 - user's ID)
HATE_RESPONSES = [
""
]

hated_user_id = None  
last_responses = []

@app.on_message(filters.command("hate", prefixes=".") & filters.user(OWNER_ID))
async def hate_user(client, message):
    global hated_user_id
    args = message.text.split(maxsplit=1)

    if len(args) == 1:  
        hated_user_id = None
        await message.reply_text("Message hate disabled")
        return

    try:
        hated_user_id = int(args[1])
        await message.reply_text(f"Now I'm hating messages {hated_user_id}")
    except ValueError:
        await message.reply_text("Error: Enter a valid user ID.")
@app.on_message(filters.text)
async def hate_reply(client, message):
    global last_responses

    if hated_user_id and message.from_user and message.from_user.id == hated_user_id:
        available_responses = list(set(HATE_RESPONSES) - set(last_responses))
        
        if not available_responses:  
            last_responses = []
            available_responses = HATE_RESPONSES.copy()
        
        response = random.choice(available_responses)
        last_responses.append(response)

        if len(last_responses) > 10: 
            last_responses.pop(0)

        await message.reply_text(response)



# Delete a certain number of messages. 
#Example:  .delete 50
@app.on_message(filters.command("delete", prefixes=".") & filters.user(OWNER_ID))
async def delete_messages(client, message):
    chat_id = message.chat.id
    try:
        count = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Error1: Missing quantity. Try again.")
        return

    deleted = 0
    async for msg in client.get_chat_history(chat_id, limit=count):
        if msg.from_user and msg.from_user.id == OWNER_ID:
            try:
                await client.delete_messages(chat_id, msg.id)
                deleted += 1
            except Exception as e:
                print(f"Message Could Not Be Deleted {msg.id}: {e}")


@app.on_message(filters.command("clear", prefixes=".") & filters.user(OWNER_ID))
async def delete_my_messages(client, message):
    chat_id = message.chat.id
    await message.delete()
    async for msg in client.get_chat_history(chat_id):
        if msg.from_user and msg.from_user.id == OWNER_ID:
            try:
                await client.delete_messages(chat_id, msg.id)
            except Exception as e:
                print(f"Message Could Not Be Deleted {msg.id}: {e}")




@app.on_message(filters.command("stop", prefixes=".") & filters.user(OWNER_ID))
async def stop_bot(client, message):
    await message.reply("The bot stops...")
    await client.stop()  
    sys.exit()  
    
@app.on_message(filters.command("reload", prefixes=".") & filters.user(OWNER_ID))
async def reload_userbot(client, message):
    await message.reply_text("Reboting userbot. Please wait...")
    logger.info("Userbot is rebooting...")  
    os.execl(sys.executable, sys.executable, *sys.argv)  

app.run()
app.start()
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.info("Userbot stopped manually or by internet connection.")
finally:
    app.stop()
    logger.info("Userbot stopped.")
