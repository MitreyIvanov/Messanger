from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtNetwork import QHostAddress

from User import User

def new_connection():
    print("Someone has been connected")
    ws = server.nextPendingConnection()
    user = User(ws=ws, parent=app)
    QTimer.singleShot(3000, user.check)
    ws.textMessageReceived.connect(user.text_message_received)
    ws.disconnected.connect(user.delete_user)

app = QCoreApplication([])
server = QWebSocketServer("", QWebSocketServer.SslMode.NonSecureMode, app)
if server.listen(address=QHostAddress.LocalHost):
    server.newConnection.connect(new_connection)
    print("The server has been launched")
    print(f"The IP of the server: {server.serverAddress().toString()}")
    print(f"The port of the server: {server.serverPort()}")
else:
    print("The launching failed")
app.exec()