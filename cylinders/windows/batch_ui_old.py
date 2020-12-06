# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'batch_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_BatchWindow(object):
    def setupUi(self, BatchWindow):
        if not BatchWindow.objectName():
            BatchWindow.setObjectName(u"BatchWindow")
        BatchWindow.resize(750, 600)
        BatchWindow.setMinimumSize(QSize(750, 600))
        BatchWindow.setBaseSize(QSize(750, 600))
        icon = QIcon(QIcon.fromTheme(u"../icons/icon.ico"))
        BatchWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(BatchWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.BatchView = QTableView(self.centralwidget)
        self.BatchView.setObjectName(u"BatchView")
        self.BatchView.setGeometry(QRect(0, 0, 531, 275))
        self.BatchView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.CurrentChanged|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.BatchView.setAlternatingRowColors(True)
        self.BatchView.setSortingEnabled(True)
        self.CylindersView = QTableView(self.centralwidget)
        self.CylindersView.setObjectName(u"CylindersView")
        self.CylindersView.setGeometry(QRect(0, 310, 531, 275))
        self.CylindersView.setAlternatingRowColors(True)
        self.AddBatchGb = QGroupBox(self.centralwidget)
        self.AddBatchGb.setObjectName(u"AddBatchGb")
        self.AddBatchGb.setGeometry(QRect(540, 0, 201, 271))
        self.SeriaLb = QLabel(self.AddBatchGb)
        self.SeriaLb.setObjectName(u"SeriaLb")
        self.SeriaLb.setGeometry(QRect(10, 20, 61, 21))
        font = QFont()
        font.setPointSize(10)
        self.SeriaLb.setFont(font)
        self.SeriaEdit = QLineEdit(self.AddBatchGb)
        self.SeriaEdit.setObjectName(u"SeriaEdit")
        self.SeriaEdit.setGeometry(QRect(70, 20, 110, 20))
        self.SufixEdit = QLineEdit(self.AddBatchGb)
        self.SufixEdit.setObjectName(u"SufixEdit")
        self.SufixEdit.setGeometry(QRect(70, 80, 110, 20))
        self.SufixLb = QLabel(self.AddBatchGb)
        self.SufixLb.setObjectName(u"SufixLb")
        self.SufixLb.setGeometry(QRect(10, 80, 61, 21))
        self.SufixLb.setFont(font)
        self.PartiaLb = QLabel(self.AddBatchGb)
        self.PartiaLb.setObjectName(u"PartiaLb")
        self.PartiaLb.setGeometry(QRect(10, 50, 61, 21))
        self.PartiaLb.setFont(font)
        self.PartiaEdit = QDateEdit(self.AddBatchGb)
        self.PartiaEdit.setObjectName(u"PartiaEdit")
        self.PartiaEdit.setGeometry(QRect(70, 50, 110, 22))
        self.addBatchButton = QPushButton(self.AddBatchGb)
        self.addBatchButton.setObjectName(u"addBatchButton")
        self.addBatchButton.setGeometry(QRect(10, 110, 170, 23))
        self.docsGb = QGroupBox(self.centralwidget)
        self.docsGb.setObjectName(u"docsGb")
        self.docsGb.setGeometry(QRect(540, 310, 201, 241))
        self.CreatePassportButton = QPushButton(self.docsGb)
        self.CreatePassportButton.setObjectName(u"CreatePassportButton")
        self.CreatePassportButton.setGeometry(QRect(10, 60, 161, 23))
        self.oldFormat_rb = QRadioButton(self.docsGb)
        self.oldFormat_rb.setObjectName(u"oldFormat_rb")
        self.oldFormat_rb.setGeometry(QRect(10, 20, 141, 17))
        self.newFormat_rb = QRadioButton(self.docsGb)
        self.newFormat_rb.setObjectName(u"newFormat_rb")
        self.newFormat_rb.setGeometry(QRect(10, 40, 141, 17))
        self.newFormat_rb.setChecked(True)
        self.CreateEtiketkaButton = QPushButton(self.docsGb)
        self.CreateEtiketkaButton.setObjectName(u"CreateEtiketkaButton")
        self.CreateEtiketkaButton.setGeometry(QRect(10, 120, 161, 23))
        self.CreateTitulnButton = QPushButton(self.docsGb)
        self.CreateTitulnButton.setObjectName(u"CreateTitulnButton")
        self.CreateTitulnButton.setGeometry(QRect(10, 90, 161, 23))
        self.CreateManyEtiketkaButton = QPushButton(self.docsGb)
        self.CreateManyEtiketkaButton.setObjectName(u"CreateManyEtiketkaButton")
        self.CreateManyEtiketkaButton.setGeometry(QRect(10, 150, 161, 23))
        self.CaptionCylinderslabel = QLabel(self.centralwidget)
        self.CaptionCylinderslabel.setObjectName(u"CaptionCylinderslabel")
        self.CaptionCylinderslabel.setGeometry(QRect(0, 280, 791, 20))
        self.CaptionCylinderslabel.setAlignment(Qt.AlignCenter)
        BatchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(BatchWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 750, 21))
        BatchWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(BatchWindow)
        self.statusbar.setObjectName(u"statusbar")
        BatchWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(BatchWindow)

        QMetaObject.connectSlotsByName(BatchWindow)
    # setupUi

    def retranslateUi(self, BatchWindow):
        BatchWindow.setWindowTitle(QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u0438 \u041a\u0413\u041c", None))
        self.AddBatchGb.setTitle(QCoreApplication.translate("BatchWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e", None))
        self.SeriaLb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u044f:", None))
        self.SufixLb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0443\u0444\u0438\u043a\u0441:", None))
        self.PartiaLb.setText(QCoreApplication.translate("BatchWindow", u"\u041f\u0430\u0440\u0442\u0438\u044f:", None))
        self.addBatchButton.setText(QCoreApplication.translate("BatchWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e", None))
        self.docsGb.setTitle(QCoreApplication.translate("BatchWindow", u"\u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432 \u043f\u043e \u043f\u0430\u0440\u0442\u0438\u0438", None))
        self.CreatePassportButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043f\u0430\u0441\u043f\u043e\u0440\u0442", None))
        self.oldFormat_rb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0442\u0430\u0440\u043e\u0433\u043e \u043e\u0431\u0440\u0430\u0437\u0446\u0430", None))
        self.newFormat_rb.setText(QCoreApplication.translate("BatchWindow", u"\u041d\u043e\u0432\u043e\u0433\u043e \u043e\u0431\u0440\u0430\u0437\u0446\u0430", None))
        self.CreateEtiketkaButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043e\u0431\u0440\u0430\u0437\u0446\u044b \u044d\u0442\u0438\u043a\u0435\u0442\u043e\u043a", None))
        self.CreateTitulnButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0442\u0438\u0442\u0443\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0441\u0442", None))
        self.CreateManyEtiketkaButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e \u044d\u0442\u0438\u043a\u0435\u0442\u043e\u043a", None))
        self.CaptionCylinderslabel.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u043e \u0441\u0435\u0440\u0438\u0438:", None))
    # retranslateUi

