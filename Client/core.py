import asyncio

from PySide6.QtWidgets import QListWidgetItem

from typesofresponse import TypesOfResponse

class User:
    text = "" # str
    id = None # str
    name = None # str
    QListWidgetItem = None # QListWidgetItem

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Core:
    ws = None  # _WSRequestContextManaged
    event_loop = None # asyncio.AbstractEventLoop

    users = [] # list, consists of User instances
    username = None # str
    myself = None

    # widgets
    msgedit_widget = None # QTextEdit
    list_widget = None # QListWidget
    msgs_widget = None # QTextEdit

    current_companion = None # User

    def init_event_loop(self):
        # call only in coroutines!
        self.event_loop = asyncio.get_running_loop()

    def init_ws(self, ws):
        self.ws = ws

    def does_user_exist(self, id):
        for user in self.users:
            if user.id == id:
                return True
        return False

    def clear(self): # думаю, надо в будущем уточнить
        self.current_companion = None
        self.ws = None
        self.users.clear()
        self.list_widget.clear()

    async def request_users_list(self): # сделал
        """
        description: requests the list of users from the server
        arguments: none
        """
        await self.ws.send_json({"type": TypesOfRespond.REQUEST_USERS_LIST.value})

    def create_user(self, id: str, name: str): # сделал
        """
        description: adds a user to the system
        arguments:  id - the id of the new user.
                    name - the name of the new user
        """
        new_user = User(id, name)
        self.users.append(new_user)
        self.add_user_into_listwidget(new_user)
        return new_user

    def add_user_into_listwidget(self, user: User): # сделал
        """
        description: adds the user to the listwidget of all the users
        arguments:  user - our user
        """
        if self.list_widget:
            user.QListWidgetItem = QListWidgetItem(user.name, self.list_widget)

    def user_disconnected(self, user: User): # сделал
        """
        description: a callback invoked when a user disconnects from the system
        arguments:  user - our user
        """
        self.delete_user(user)

    def remove_item_from_listwidget(self, user: User): # сделал
        """
        description: removes the user's item from the list_widget containing all users. If successfully, return True and False if is in contrary.
        arguments:  user - our user
        """
        item = user.QListWidgetItem
        if user.QListWidgetItem:
            row = self.list_widget.row(item)
            user.QListWidgetItem = None
            result = self.list_widget.takeItem(row)
            return (result and True) or False
        return False


    def delete_user(self, user: User): # переделываю в более короткий код через .remove, но через него могут быть проблемы
        """
        description: deletes a user. It returns True if the user is deleted and false if he isn't
        arguments:  user - an instance of the User class
        """
        try:
            self.users.remove(user)
        except ValueError:
            self.remove_item_from_listwidget(user)
            return False
        self.remove_item_from_listwidget(user)
        return True
        """for i, v in enumerate(self.users):           # старый код, но рабочий, кроме удаления виджета 
            if v is user:
                if user.QListWidgetItem:
                    print("Удаляем QListWidgetItem")
                    self.list_widget.removeItemWidget(user.QListWidgetItem)
                self.users.pop(i)
                return True
        return False"""

    def get_user_by_id(self, id: str): # сделал
        """
        description: gets a instance of the User class and returns it. If nothing is found, returns None
        arguments:  id - the user's id
        """
        for user in self.users:
            if user.id == id:
                return user
        return None

    def add_message(self, text: str, user_with: User, is_myself=False): #здесь проблема
        """
        description: adds a new message into the GUI and also keeps it in the memory
        arguments:  user_with - an instance of the User object of sender.
                    text - the text of a message
        """
        user_with.text += f"<b>({(is_myself and self.myself.name) or user_with.name}):</b> {text}<br>"
        if self.current_companion is user_with:
            self.msgs_widget.append(f"<b>({(is_myself and self.myself.name) or user_with.name}):</b> {text}")

    def update_users(self, users: list): # ГОВНОКОД
        """
        description: updates the list of all users. It is used when the client gets a list of users from the server.
        arguments: users - a list of users. Example: [{"id": "3d98f7ee-a73a-490d-8256-144947b2c390", "name": "Petya"},
            {"id": "3d98f7ee-a73a-490d-8256-144947b2c393", "name": "Vova"}]
        """
        self.users.clear()
        if self.list_widget:
            self.list_widget.clear()
        for user in users:
            new_user = User(user["id"], user["name"])
            if user["name"] == self.username:
                self.myself = new_user
            self.users.append(new_user)
            self.add_user_into_listwidget(new_user)

    async def send_msg(self): # вроде сделал
        """
        description: sends a message to the user. While sending only the id is used
        arguments:  none
        """
        text = self.msgedit_widget.toPlainText().rstrip()
        if text and self.current_companion:
            #self.msgedit_widget.clear() #надо разобраться, почему крашит
            await self.ws.send_json(
                {"type": TypesOfRespond.SEND_MSG.value,
                 "data": {"dest_id": self.current_companion.id, "text": text}}) #используем id пользователя, когда отправляем ему сообщение.

    async def connect(self): # сделал вроде
        """
        description: sends a request to join to the server
        arguments:  none
        """
        await self.ws.send_json({"type": TypesOfRespond.INITIALIZE.value, "data": {"name": self.username}})

    def change_text_in_msgs(self, user: User): # делаю тут сделал экспериментальные изменения
        """
        description: change the text in the QTextEdit widget containing all the conversation's messages. Return True if changed
            and false in contrary
        arguments:  user - our user
        """
        if self.msgs_widget:
            #self.msgs_widget.clear()
            self.msgs_widget.setText(user.text)
            return True
        return False

    def current_companion_changed(self, new_companion: QListWidgetItem, prev_companion: QListWidgetItem):
        #сделал, но не совсем понятно, что будет, если все пользователи исчезнут, хотя вроде ничего произойти и не должно
        #есть какая-то ошибка, QListWidgetItem всегда один и тот же. Надо проверить, присваивание QListWidget
        """
        description: a collback, it is invoked when the selection of a user changed
        arguments:  new_companion - the new choice
                    prev_companion - the previous choice
        """
        #print(new_companion)
        #print([(user.QListWidgetItem, user.name) for user in self.users])
        for user in self.users:
            #print(user.QListWidgetItem)
            if user.QListWidgetItem is new_companion:
                self.current_companion = user
                self.change_text_in_msgs(self.current_companion)
                return


    def __init__(self, username, port: int):
        self.username = username
        self.port = port
