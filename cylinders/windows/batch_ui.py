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
        BatchWindow.resize(750, 611)
        BatchWindow.setMinimumSize(QSize(750, 600))
        BatchWindow.setBaseSize(QSize(750, 600))
        self.centralwidget = QWidget(BatchWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.TabObject = QTabWidget(self.centralwidget)
        self.TabObject.setObjectName(u"TabObject")
        self.TabObject.setGeometry(QRect(0, 0, 741, 571))
        self.tab_gas = QWidget()
        self.tab_gas.setObjectName(u"tab_gas")
        self.CylindersView = QTableView(self.tab_gas)
        self.CylindersView.setObjectName(u"CylindersView")
        self.CylindersView.setGeometry(QRect(0, 310, 531, 275))
        self.CylindersView.setAlternatingRowColors(True)
        self.AddBatchGb = QGroupBox(self.tab_gas)
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
        self.addBatchButton.setGeometry(QRect(10, 150, 170, 23))
        self.PassportNoLb = QLabel(self.AddBatchGb)
        self.PassportNoLb.setObjectName(u"PassportNoLb")
        self.PassportNoLb.setGeometry(QRect(10, 110, 81, 21))
        self.PassportNoLb.setFont(font)
        self.PassportNoEdit = QLineEdit(self.AddBatchGb)
        self.PassportNoEdit.setObjectName(u"PassportNoEdit")
        self.PassportNoEdit.setGeometry(QRect(99, 110, 81, 20))
        self.docsGb = QGroupBox(self.tab_gas)
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
        self.BatchView = QTableView(self.tab_gas)
        self.BatchView.setObjectName(u"BatchView")
        self.BatchView.setGeometry(QRect(0, 0, 531, 275))
        self.BatchView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.CurrentChanged|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.BatchView.setAlternatingRowColors(True)
        self.BatchView.setSortingEnabled(True)
        self.CaptionCylinderslabel = QLabel(self.tab_gas)
        self.CaptionCylinderslabel.setObjectName(u"CaptionCylinderslabel")
        self.CaptionCylinderslabel.setGeometry(QRect(0, 280, 791, 20))
        self.CaptionCylinderslabel.setAlignment(Qt.AlignCenter)
        self.TabObject.addTab(self.tab_gas, "")
        self.tab_liquid = QWidget()
        self.tab_liquid.setObjectName(u"tab_liquid")
        self.line_edit_batch = QLineEdit(self.tab_liquid)
        self.line_edit_batch.setObjectName(u"line_edit_batch")
        self.line_edit_batch.setGeometry(QRect(100, 10, 113, 20))
        self.line_edit_batch.setAlignment(Qt.AlignCenter)
        self.label_batch = QLabel(self.tab_liquid)
        self.label_batch.setObjectName(u"label_batch")
        self.label_batch.setGeometry(QRect(0, 10, 101, 21))
        self.line_edit_count = QLineEdit(self.tab_liquid)
        self.line_edit_count.setObjectName(u"line_edit_count")
        self.line_edit_count.setGeometry(QRect(100, 40, 113, 20))
        self.line_edit_count.setAlignment(Qt.AlignCenter)
        self.label_count = QLabel(self.tab_liquid)
        self.label_count.setObjectName(u"label_count")
        self.label_count.setGeometry(QRect(0, 40, 101, 21))
        self.submit_button = QPushButton(self.tab_liquid)
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setGeometry(QRect(10, 70, 201, 23))
        self.TabObject.addTab(self.tab_liquid, "")
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

        self.TabObject.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(BatchWindow)
    # setupUi

    def retranslateUi(self, BatchWindow):
        BatchWindow.setWindowTitle(QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u0438", None))
        self.AddBatchGb.setTitle(QCoreApplication.translate("BatchWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e", None))
        self.SeriaLb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u044f:", None))
        self.SufixLb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0443\u0444\u0438\u043a\u0441:", None))
        self.PartiaLb.setText(QCoreApplication.translate("BatchWindow", u"\u041f\u0430\u0440\u0442\u0438\u044f:", None))
        self.addBatchButton.setText(QCoreApplication.translate("BatchWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e", None))
        self.PassportNoLb.setText(QCoreApplication.translate("BatchWindow", u"\u2116 \u041f\u0430\u0441\u043f\u043e\u0440\u0442\u0430:", None))
        self.docsGb.setTitle(QCoreApplication.translate("BatchWindow", u"\u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432 \u043f\u043e \u043f\u0430\u0440\u0442\u0438\u0438", None))
        self.CreatePassportButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043f\u0430\u0441\u043f\u043e\u0440\u0442", None))
        self.oldFormat_rb.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0442\u0430\u0440\u043e\u0433\u043e \u043e\u0431\u0440\u0430\u0437\u0446\u0430", None))
        self.newFormat_rb.setText(QCoreApplication.translate("BatchWindow", u"\u041d\u043e\u0432\u043e\u0433\u043e \u043e\u0431\u0440\u0430\u0437\u0446\u0430", None))
        self.CreateEtiketkaButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043e\u0431\u0440\u0430\u0437\u0446\u044b \u044d\u0442\u0438\u043a\u0435\u0442\u043e\u043a", None))
        self.CreateTitulnButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0442\u0438\u0442\u0443\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0441\u0442", None))
        self.CreateManyEtiketkaButton.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u043f\u0430\u0440\u0442\u0438\u044e \u044d\u0442\u0438\u043a\u0435\u0442\u043e\u043a", None))
        self.CaptionCylinderslabel.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u043e \u0441\u0435\u0440\u0438\u0438:", None))
        self.TabObject.setTabText(self.TabObject.indexOf(self.tab_gas), QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u0438 \u041a\u0413\u041c", None))
        self.label_batch.setText(QCoreApplication.translate("BatchWindow", u"\u0421\u0435\u0440\u0438\u044f", None))
        self.line_edit_count.setText(QCoreApplication.translate("BatchWindow", u"8", None))
        self.label_count.setText(QCoreApplication.translate("BatchWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e, \u0442.", None))
        self.submit_button.setText(QCoreApplication.translate("BatchWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.TabObject.setTabText(self.TabObject.indexOf(self.tab_liquid), QCoreApplication.translate("BatchWindow", u"\u041a\u0416\u041c", None))
    # retranslateUi

