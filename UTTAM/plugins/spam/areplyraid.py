import os
import sys
import asyncio
import re
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.data import *
from UTTAM.database.rraid import *
from UTTAM import SUDO_USER
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message

DEVS = int(5738579437)  # Bot Owner ID
from UTTAM.helper.PyroHelpers import get_ub_chats
from UTTAM.plugins.basic.profile import extract_user, extract_user_and_reason

SUDO_USERS = SUDO_USER
from .replyraid import RAIDS

@Client.on_message(filters.command("replyraid"))  # 👈 Sab users ke liye enable
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")
    
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ex.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ex.edit(f"`Please specify a valid user!`")
        return

    if user.id == client.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")
    elif user.id in SUDO_USERS:
        return await ex.edit("**Okay But Failed Because this user is in SUDO_USERS.. 🐽**")
    
    try:
        if user.id in (await get_rraid_users()):
            await ex.edit("Replyraid is already activated on this user")
            return

        await rraid_user(user.id)
        RAIDS.append(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) Activated ReplyRaid!")
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")