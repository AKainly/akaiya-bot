import asyncio
import logging
import time
import datetime
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN

PNG_TAGS = ["waifu", "neko", "shinobu"]
GIF_TAGS = ["bully", "cry", "hug", "lick", "pat", "nom", "slap", "dance", "poke", "cringe", "bite", "blush", "smug", "wink", "highfive"]
ALL_TAGS = PNG_TAGS + GIF_TAGS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
last_command_time = {}
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = str(message.from_user.id)
    nickname = message.from_user.first_name
    username = message.from_user.username
    current_time = datetime.datetime.now()

    if user_id in last_command_time:
        time_difference = (current_time - last_command_time[user_id]).total_seconds()
        if time_difference < 3:
            return
    last_command_time[user_id] = current_time

    welcome_text = (
        f'*👋 Приветствую, {nickname}!* \n\n'
        'akaiya – это Telegram-бот, который позволит вам получать уникальные аниме-изображения и GIF по запросу. Используйте команды `/start` и `/anime`, чтобы начать работу с ботом.\n\n'
    )

    await message.answer(welcome_text, parse_mode="Markdown")
    logger.info(f"{nickname} | @{username} - ID: {user_id} - Command: /start")


@dp.message(Command("anime"))
async def anime_command(message: types.Message):
    user_id = message.from_user.id
    nickname = message.from_user.full_name
    username = message.from_user.username
    parts = message.text.split()

    current_time = time.time()
    if user_id in last_command_time:
        time_diff = current_time - last_command_time[user_id]
        if time_diff < 1:
            await message.reply("Подождите немного перед повторным запросом.")
            return
    last_command_time[user_id] = current_time

    if len(parts) == 1:
        await message.reply(get_tags_description(), parse_mode="Markdown")
        logger.info(f"{nickname} | @{username} - ID: {user_id} - Command: /anime")
        return

    tag = parts[1].lower()

    if tag == "random":
        image_url = await get_random_image_from_second_api()
        if image_url:
            await message.reply_photo(image_url, caption="🍂 Вот ваше случайное изображение!")
            logger.info(f"{nickname} | @{username} - ID: {user_id} - Command: /anime random")
        else:
            await message.reply("Не удалось получить случайное изображение. Попробуйте позже.")
        return

    if tag not in ALL_TAGS:
        await message.reply("Некорректный тег! Используйте команду /anime, чтобы увидеть доступные теги.")
        logger.warning(f"{nickname} | @{username} - ID: {user_id} - Command: /anime {tag}")
        return

    image_url = await get_image_from_api(tag)
    if image_url:
        await message.reply_photo(image_url, caption="🍂 Вот изображение по вашему запросу!")
        logger.info(f"{nickname} | @{username} - ID: {user_id} - Command: /anime {tag}")
    else:
        await message.reply("Не удалось получить изображение по вашему запросу. Попробуйте позже.")


async def get_image_from_api(tag: str) -> str:
    url = f"https://api.waifu.pics/sfw/{tag}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("url")
                logger.error(f"API вернул статус {response.status} для тега: {tag}")
                return None
    except Exception as e:
        logger.exception(f"Ошибка при запросе изображения: {e}")
        return None


async def get_random_image_from_second_api() -> str:
    base_url = "https://pic.re/image"
    unique_url = f"{base_url}?{int(time.time())}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(unique_url) as response:
                if response.status == 200:
                    return str(response.url)
                logger.error(f"Ошибка при запросе к API: {response.status}")
                return None
    except Exception as e:
        logger.exception(f"Ошибка при запросе случайного изображения: {e}")
        return None


def get_tags_description() -> str:
    logger.info("Запрошено описание доступных тегов")
    return (
        "*📚 Используйте команду* `/anime <tag>` *или* `/anime random`, *чтобы получить изображение или GIF с определённым тегом.*\n\n"
        "*- Изображение*:\n"
        f"{', '.join(PNG_TAGS)}\n\n"
        "*- GIF*:\n"
        f"{', '.join(GIF_TAGS)}\n\n"
        "*- Other*:\n"
        "random."
    )


async def main():
    await bot.get_updates(offset=-1)
    logger.info("Бот запущен!")
    try:
        await dp.start_polling(bot, skip_updates=True, request_timeout=90)
    except asyncio.CancelledError:
        logger.info("Бот выключился!")
    except Exception as e:
        logger.error("Ошибка при запуске: %s", str(e))


if __name__ == "__main__":
    asyncio.run(main())
