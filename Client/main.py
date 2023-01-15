import asyncio
import json
from threading import Thread

from PySide6.QtWidgets import QApplication
import aiohttp

from mainwindow import Mainwindow
from core import Core, User
from typesofresponse import TypesOfResponse, TypesOfSuccess


async def main():
    core.init_event_loop()

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url=('ws://127.0.0.1:' + str(core.port))) as ws:
            core.init_ws(ws)
            await core.connect()
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    answer = json.loads(msg.data)

                    match TypesOfRespond(answer["type"]):
                        case TypesOfRespond.SUCCESS: # сделал
                            # answer = {"type": TypesOfRespond.SUCCESS.value, "what": TypesOfSuccess.MSG_SEND.value}
                            match TypesOfSuccess(answer["what"]):
                                case TypesOfSuccess.INITIALIZATION:
                                    # answer = {"type": TypesOfRespond.SUCCESS.value, "what": TypesOfSuccess.INITIALIZATION}
                                    await core.request_users_list()
                                case TypesOfSuccess.MSG_SEND: #доделать
                                    # answer = {"type": TypesOfRespond.SUCCESS.value, "what": TypesOfSuccess.MSG_SEND,
                                    #                                  "data": {"text": text, "id_with": 2342423454}}
                                    user_with = core.get_user_by_id(answer["data"]["id_with"])
                                    if user_with:
                                        core.add_message(answer["data"]["text"], user_with, True)


                        case TypesOfRespond.USER_CONNECTED: # сделал
                            # answer = {"type": type.value, "data": {"user": self.user_dict}}
                            core.create_user(answer["data"]["user"]["id"], answer["data"]["user"]["name"])
                        case TypesOfRespond.USER_DISCONNECTED: # сделал
                            # {"type": TypesOfRespond.USER_DISCONNECTED.value, "data": {"user": self.user_dict}}
                            user = core.get_user_by_id(answer["data"]["user"]["id"])
                            if user:
                                core.user_disconnected(user)
                        case TypesOfRespond.GETTING_USERS: # сделал
                            # answer = {"type": TypesOfRespond.GETTING_USERS.value, "data": {"users": list_for_sending}}
                            core.update_users(answer["data"]["users"])
                        case TypesOfRespond.INCOMING_MESSAGE: #сделал вроде
                            # answer = {"type": TypesOfRespond.INCOMING_MESSAGE.value,
                            #                                                "data": {"text": text, "from": self.user_dict}}
                            #print("new message", answer["data"]["text"], "by", answer["data"]["from"]["id"])
                            user = core.get_user_by_id(answer["data"]["from"]["id"])
                            if not user:
                                user = core.create_user(answer["data"]["from"]["id"], answer["data"]["from"]["name"])
                            core.add_message(answer["data"]["text"], user)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

            core.clear()

core = Core(input("Введите имя пользователя: "), int(input("Введите порт сервера: ")))
a = QApplication([])
ab = Mainwindow(core)
ab.show()
Thread(target=lambda: asyncio.run(main()), daemon=True).start()
a.exec()
