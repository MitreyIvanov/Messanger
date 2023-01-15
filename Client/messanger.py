# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        if not mainwindow.objectName():
            mainwindow.setObjectName(u"mainwindow")
        mainwindow.resize(809, 655)
        self.users = QListWidget(mainwindow)
        self.users.setObjectName(u"users")
        self.users.setGeometry(QRect(10, 10, 201, 631))
        self.msgs = QTextEdit(mainwindow)
        self.msgs.setObjectName(u"msgs")
        self.msgs.setGeometry(QRect(220, 10, 581, 551))
        self.msgs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.msgs.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.msgs.setReadOnly(True)
        self.msgs.setOverwriteMode(False)
        self.msgedit = QTextEdit(mainwindow)
        self.msgedit.setObjectName(u"msgedit")
        self.msgedit.setGeometry(QRect(220, 570, 441, 71))
        self.sendbtn = QPushButton(mainwindow)
        self.sendbtn.setObjectName(u"sendbtn")
        self.sendbtn.setGeometry(QRect(670, 570, 131, 71))
        self.sendbtn.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.retranslateUi(mainwindow)

        QMetaObject.connectSlotsByName(mainwindow)
    # setupUi

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(QCoreApplication.translate("mainwindow", u"Form", None))
        self.msgs.setHtml(QCoreApplication.translate("mainwindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.sendbtn.setText(QCoreApplication.translate("mainwindow", u"Send message", None))
    # retranslateUi

