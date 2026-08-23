import os
import aiohttp

ARC_APIS = [
    os.getenv("ARC_API_1"),
    os.getenv("ARC_API_2"),
    os.getenv("ARC_API_3"),
]


async def search_arc(query):
    for api in ARC_APIS:
        if not api:
            continue

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    api,
                    params={"query": query}
                ) as resp:

                    if resp.status == 200:
                        data = await resp.json()

                        if data:
                            return data

        except Exception:
            continue

    return None
