import aiohttp
import asyncio
import os, time
from pyrogram import Client, filters
apiid=os.getenv("apiid")
apih=os.getenv("apihash")
tk=os.getenv("tk")

plugins = dict(root="plugins")
bot = Client(name="RVX_bot", bot_token=tk, api_id=apiid, api_hash=apih,plugins=plugins)

    # Run the bot
bot.run()

# Run the async event loop

