import logging
from os import getenv
from pprint import pprint

from dotenv import load_dotenv

load_dotenv('.env_sending')

from aiogram import Bot, F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# from aiogram.fsm.context import FSMContext
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
main_aiogram_router = Router()
from fsm import UserState
from keyBoards import mainMenu
from main import bot

# from local_cache import memory_dict


# TODO: Вот этот запрос бы прикрутить к готовеньким bot, Dispatcher


async def send_response_from_bot_to_user(user_chat_id, message_text, reply_to_msg_id):
    # print("send_response_from_bot_to_user")
    # dp = Dispatcher(storage=MemoryStorage())

    await bot.send_message(chat_id=user_chat_id,
                           text=message_text,
                           reply_to_message_id=reply_to_msg_id)


    #TODO Как логи то нормально сделать в асинхр?
    # await logging.INFO(f"send_response_from_bot_to_user. We have resend response from coze_bot to user")
    await bot.close()

#________________ Стандартные ручки aiogram


@main_aiogram_router.message(Command("start"))
async def start_handler(message: Message, state: UserState):
    logging.info("☄️ i see start command")
    # global memory_dict
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=mainMenu)
    # await state.set_state(UserState.FREE_TRIAL)
    # await state.update_data(test_atr="testStr")
    # memory_dict.update(dict123=123)
    # print(memory_dict)

# @router
# async def gosurf_handler(message: Message):
#     print("gosurf_handler")
#     print(message.text)
#     print(message)
    # await send_msg_to_coze_bot_via_tg(message=message.text,
    #                                   user_chat_id=message.chat.id,
    #                                   user_message_id=message.message_id)


@main_aiogram_router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")


@main_aiogram_router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()


# @router.update()
# def router_get_updates(message: Message):
#     pprint(message)
#     pass


@main_aiogram_router.message()
async def message_handler(message: Message):
    pprint(message)
    if message.from_user.id != 6927113111:
        await send_msg_to_coze_bot_via_tg(message=message.text,
                                          user_chat_id=message.chat.id,
                                          user_message_id=message.message_id)
