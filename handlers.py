from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from telethon import TelegramClient, sync, events
telethron_chat_for_exchenge_with_china = getenv('telethron_chat_for_exchenge_with_china')

from database import add_new_user
from neuroThings import add_user_messege_and_run

from keyBoards import mainMenu, openAIpoll



router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=mainMenu)
    add_new_user(message.from_user.id, message.from_user.full_name)

@router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    await message.reply("Профиль")

@router.message(F.text == "Меню")
async def menu(message: Message):
    await message.answer('Привет, вот меню', reply_markup=mainMenu)

# Отвечать openAI
@router.message()
async def message_handler(message: Message):
    user_id = message.from_user.id
    thread_id = "thread_tjXAUQjpkW5E824feP25CIlR"
    if thread_id: # Убедились, что доступ есть.
        # print(thread_id, message.text)
        responce_from_openAI = add_user_messege_and_run(thread_id, message.text)
        await message.reply(responce_from_openAI, reply_markup=openAIpoll)
    else:
        await message.answer("На сегодня бесплатные запросы закончились. Приходите завтра или оплатите подписку",
                             reply_markup=mainMenu)


@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()







#Ручки тг клиента


async def send_msg_to_china(client, messege ):
    messege = "@neuro44fz_bot " + messege
    print("Сча будем засылать в чат: " + str(telethron_chat_for_exchenge_with_china))
    send_message_to_china = await client.send_message(telethron_chat_for_exchenge_with_china, messege)
    id_message_to_china = send_message_to_china.to_dict()["id"]
    print("Сообщение отправили, его id:" + str(id_message_to_china))
    # return id_message_to_china
    # for dialog in client.iter_dialogs():
    #     print(dialog)

@events.register(events.MessageEdited(chats=telethron_chat_for_exchenge_with_china))
async def i_see_edits_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']
    # print(arr[0])   #.message.to_dict()['message']

@events.register(events.NewMessage(chats=telethron_chat_for_exchenge_with_china))
async def i_see_response_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']

    # print(arr[0])   #.message.to_dict()['message']


@events.register(events.NewMessage(chats=('v_karpyuk')))
async def start_go_test_handler(event):
    if str(event.message.to_dict()['message']).startswith("Го") or str(event.message.to_dict()['message']).startswith("Uj"):
        print("Погнали")
        client = event.client
        await send_msg_to_china(client, "Что такое обеспечение заявки")

        # send_message_to_china = await client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
        # id_message_to_china = send_message_to_china.to_dict()["id"]
        # print(send_message_to_china.to_dict()["id"])

        pass

