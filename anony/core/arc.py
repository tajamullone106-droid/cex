import os
import re
import aiohttp
from dotenv import load_dotenv
from anony import userbot

load_dotenv("/home/ubuntu/cex/.env")

ARC_URL = os.getenv("ARC_API_URL", "https://api.arcmusic.fun")
ARC_KEY = os.getenv("ARC_API_KEY")


async def download(query):
    try:
        api = ARC_URL.rstrip("/") + "/youtube/v2/download"

        params = {
            "query": query,
            "api_key": ARC_KEY
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(api, params=params) as resp:
                data = await resp.json()

        cdn = data.get("result", {}).get("cdn")

        if not cdn:
            return None

        match = re.search(r"t\.me/([^/]+)/(\d+)", cdn)

        if not match:
            return None

        chat = match.group(1)
        msg_id = int(match.group(2))

        client = userbot.clients[0]

        msg = await client.get_messages(chat, msg_id)

        if not msg:
            return None

        file_path = await client.download_media(
            msg,
            file_name=f"downloads/{msg.id}.webm"
)

        return file_path

    except Exception as e:
        print("ARC ERROR:", e)
        return None
