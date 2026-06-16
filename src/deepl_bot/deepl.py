import asyncio
import aiohttp

from decouple import config

DEEPL_TOKEN = config("DEEPL_TOKEN")

API_URL = "https://api-free.deepl.com"

HEADERS = {"Authorization": f"DeepL-Auth-Key {DEEPL_TOKEN}"}

langs = {}


async def translate_text(text: str, target_lang: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{API_URL}/v2/translate",
                    headers=HEADERS,
                    data={
                        "text": [text],
                        "target_lang": target_lang,
                        "enable_beta_languages": True
                    },
                    timeout=aiohttp.ClientTimeout(total=120),
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
        source_lang = data["translations"][0]["detected_source_language"]
        n = min(3, len(source_lang), len(target_lang))
        if not source_lang or source_lang[:n] == target_lang[:n]:
            return None
        return data["translations"][0]["text"]

    except asyncio.TimeoutError:
        return "⚠️ The server seems to be down now. Try again in a couple of minutes"

    except Exception as e:
        print(e)
        return "⚠️ Something went wrong. Try again in a couple of minutes"


async def get_languages() -> None:
    global langs

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{API_URL}/v2/languages",
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=120),
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

    langs = {language["language"]: language["name"] for language in data}
