import threading
import asyncio

from PySide6.QtWidgets import QWidget

from messanger import Ui_mainwindow

class Mainwindow(QWidget):
    def __init__(self, core):
        super().__init__()
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)
        self.setFixedSize(809, 655)
        self.setWindowTitle(core.username)

        # всякие слоты и сигналы
        self.ui.sendbtn.clicked.connect(lambda: asyncio.run_coroutine_threadsafe(core.send_msg(), core.event_loop))
        self.ui.users.currentItemChanged.connect(core.current_companion_changed)

        core.msgedit_widget = self.ui.msgedit
        core.list_widget = self.ui.users
        core.msgs_widget = self.ui.msgs