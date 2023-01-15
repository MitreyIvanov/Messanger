import json
import uuid

from PySide6.QtCore import QObject
from PySide6.QtWebSockets import QWebSocket

from TypesOfRespond import TypesOfRespond, TypesOfSuccess

MAX_NAME_LENGTH = 20

users = []

def is_user_exists_by_name(name: str): # сделал
    """
    descriptor: checks if there is the user with such name.
    argument:   name - the name of a user.
    """
    for user in users:
        if user.name == name: return True
    return False

def get_user_by_id(id: str): # сделал
    """
    descriptor: return the User instance by an id.
    arguments:  id - the id of a user
    """
    for user in users:
        if user.id == id:
            return user
    return None

class Ws(): # наверное, неправильно поступил
    ws = None
    def __init__(self, ws):
        self.ws = ws

    def send_json(self, data):
        self.ws.sendTextMessage(json.dumps(data))

    def close(self):
        self.ws.close()

class User(QObject):
    name = None
    id = None
    ws = None
    user_dict = None

    def __init__(self, ws, parent):
        super().__init__(parent)
        self.ws = Ws(ws)

    def text_message_received(self, text):
        answer = json.loads(text)
        match TypesOfRespond(answer["type"]):
            case TypesOfRespond.INITIALIZE:  # сделал
                # answer = {"type": TypesOfRespond.INITIALIZE.value, "data": {"name": self.username}}
                self.set_name(answer["data"]["name"])

            case TypesOfRespond.SEND_MSG:  # ДЕЛАЮ, ВОЗНИКАЕТ ОШИБКА, ЧТО ОТПРАВИТЕЛЬ НЕ ТОТ
                # answer = {"type": TypesOfRespond.SEND_MSG.value,
                #                  "data": {"dest_id": self.current_companion.id, "text": text}}
                print("We have got a message, sending it to destination")
                user_dest = get_user_by_id(answer["data"]["dest_id"])
                # print(user_from)
                if user_dest:
                    user_dest.send_msg(self, answer["data"]["text"])
                    if user_dest is not self:
                        self.success_send_msg(answer["data"]["text"], user_dest)

            case TypesOfRespond.REQUEST_USERS_LIST:  # сделал
                print("The user has requested a list of users")
                self.send_users_list()

    def set_name(self, name: str): # сделал
        """
        description: set the name to the user, e.g. initializes him. It can raise an error if the name doesn't fit.
        arguments:  name - the name to use
        """
        # нужно в будущем доделать причины ошибок и сделать их с Enum
        name = name.strip()

        if self.name: return    # if the user has already logged in
        elif not name:              # if there is no name
            self.ws.send_json({"type": TypesOfRespond.ERROR.value, "data": {"reason": "name_is_empty"}})
            self.ws.close()
            return
        elif len(name) > MAX_NAME_LENGTH:        # if the name is too long
            self.ws.sendTextMessage({"type": TypesOfRespond.ERROR.value, "data": {"reason": "name_too_long"}})
            self.ws.close()
            return
        elif is_user_exists_by_name(name):  # if the user with such name is already exists
            self.ws.send_json({"type": TypesOfRespond.ERROR.value, "data": {"reason": "name_taken"}})
            self.ws.close()
            return

        self.name = name
        self.id = str(uuid.uuid4())
        users.append(self)
        self.user_dict = {
            "id": self.id,
            "name": self.name
        }
        self.success_initialization()
        self.tell_all(TypesOfRespond.USER_CONNECTED)
        print(self.name + " has been connected and initialized")

    def success_initialization(self):
        """
        description: tells the user that he has been successfully initialized on the server
        arguments: none
        """
        self.ws.send_json({"type": TypesOfRespond.SUCCESS.value, "what": TypesOfSuccess.INITIALIZATION.value})

    def success_send_msg(self, text: str, user_with):
        self.ws.send_json({"type": TypesOfRespond.SUCCESS.value, "what": TypesOfSuccess.MSG_SEND.value,
                                 "data": {"text": text, "id_with": user_with.id}})

    def send_users_list(self):
        """
        description: form a list of all users and sends it to the user. An example of list
            [{"id": "3d98f7ee-a73a-490d-8256-144947b2c390", "name": "Petya"},
            {"id": "3d98f7ee-a73a-490d-8256-144947b2c393", "name": "Vova"}]
        arguments: none
        """
        if self.name:
            list_for_sending = [{"id": user.id, "name": user.name} for user in users]
            print("Sending list of users")
            self.ws.send_json({"type": TypesOfRespond.GETTING_USERS.value, "data": {"users": list_for_sending}})

    def tell_all(self, type):
        """
        description: tells all the users (except our user) that a new user has been connected. type - is Enum
        arguments:  type - type of what the user has done
        """
        if self.name:
            for user in users:
                if user is not self:
                    user.ws.send_json({"type": type.value, "data": {"user": self.user_dict}})

    def send_msg(self, from_user, text: str): #сделал
        """
        description: sends a message to the user.
        arguments:  from_user - the user that has sent a message
                    text - the text of a message
        """
        self.ws.send_json({"type": TypesOfRespond.INCOMING_MESSAGE.value,
                                           "data": {"text": text, "from": from_user.user_dict}})

    def delete_user(self): # сделал
        """
        description: removes the user from the system. It is used in the end of the handler, when the connected is over.
            It is the desctructor of the class.
        arguments: none
        """
        if self.name:
            print(self.name + " has been disconnected")
            self.tell_all(TypesOfRespond.USER_DISCONNECTED)
            try:
                users.remove(self)
            except ValueError:
                pass
            self.deleteLater()

    def check(self):
        if not self.name:
            print("Time is up, but the user hasn't been authorized")
            self.ws.close()
            self.deleteLater()