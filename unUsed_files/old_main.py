from fastapi import FastAPI
from contextlib import asynccontextmanager

from loguru import logger
from os import getenv
from dotenv import load_dotenv

load_dotenv('../.venv/.env')
env_server_mode = getenv('env_server_mode')

env_main_tg_bot_token = getenv('env_main_tg_bot_token')

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"

env_db_host = getenv('env_db_host')
env_db_username = getenv('env_db_username')
env_db_pass = getenv('env_db_pass')
env_db_name = getenv('env_db_name')

# cache_dict = dict()
# cache_dict = {'dict': 1, 'dictionary': 2}

from routes_FastAPI import root_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    from main_bot_iaogram.main_aiogramm_bot import start_telegram
    await start_telegram()
    yield
    logger.info("⛔ Stopping application")

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)













#
# async def main_aiogram_bot():
#     bot = Bot(token=env_main_tg_bot_token, parse_mode=ParseMode.HTML)
#     # dp = Dispatcher(storage=MySQLStorage(host=env_db_host,
#     #                                      user=env_db_username,
#     #                                      database=env_db_name,
#     #                                      password=env_db_pass,
#     #                                      bot=bot))
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#
#
#
# async def main_telethron_bot():
#     client_telethron = TelegramClient(session=".venv/session_name.session",
#                                       api_id=int(env_telethon_api_id),
#                                       api_hash=env_telethon_api_hash)
#     client_telethron.add_event_handler(i_see_response_handler)
#     client_telethron.add_event_handler(i_see_edits_handler)
#     client_telethron.add_event_handler(start_go_test_handler)
#     await client_telethron.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
#     try:
#         await client_telethron.run_until_disconnected()
#     finally:
#         await client_telethron.disconnect()
#
#
#
# async def main():
#     await asyncio.gather(main_telethron_bot(),main_aiogram_bot())   # m
#
#
# if __name__ == "__main__":
#     logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#                         level=logging.INFO)
#     if env_server_mode=="PROD":
#         asyncio.run(main())
#     elif env_server_mode=="TEST":
#         asyncio.run(main())