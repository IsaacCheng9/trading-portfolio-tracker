# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transaction_history.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QDialog,
    QFrame, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_dialog_transaction_history(object):
    def setupUi(self, dialog_transaction_history):
        if not dialog_transaction_history.objectName():
            dialog_transaction_history.setObjectName(u"dialog_transaction_history")
        dialog_transaction_history.resize(1000, 800)
        font = QFont()
        font.setPointSize(12)
        dialog_transaction_history.setFont(font)
        self.verticalLayoutWidget = QWidget(dialog_transaction_history)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 6, 981, 781))
        self.vert_layout_dialog = QVBoxLayout(self.verticalLayoutWidget)
        self.vert_layout_dialog.setObjectName(u"vert_layout_dialog")
        self.vert_layout_dialog.setContentsMargins(0, 0, 0, 0)
        self.lbl_transaction_history = QLabel(self.verticalLayoutWidget)
        self.lbl_transaction_history.setObjectName(u"lbl_transaction_history")
        font1 = QFont()
        font1.setPointSize(22)
        self.lbl_transaction_history.setFont(font1)

        self.vert_layout_dialog.addWidget(self.lbl_transaction_history)

        self.hori_line_transaction_header = QFrame(self.verticalLayoutWidget)
        self.hori_line_transaction_header.setObjectName(u"hori_line_transaction_header")
        self.hori_line_transaction_header.setFrameShape(QFrame.HLine)
        self.hori_line_transaction_header.setFrameShadow(QFrame.Sunken)

        self.vert_layout_dialog.addWidget(self.hori_line_transaction_header)

        self.table_widget_portfolio = QTableWidget(self.verticalLayoutWidget)
        if (self.table_widget_portfolio.columnCount() < 9):
            self.table_widget_portfolio.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_widget_portfolio.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.table_widget_portfolio.setObjectName(u"table_widget_portfolio")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_widget_portfolio.sizePolicy().hasHeightForWidth())
        self.table_widget_portfolio.setSizePolicy(sizePolicy)
        self.table_widget_portfolio.setFont(font)
        self.table_widget_portfolio.setFrameShape(QFrame.StyledPanel)
        self.table_widget_portfolio.setFrameShadow(QFrame.Sunken)
        self.table_widget_portfolio.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table_widget_portfolio.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_portfolio.setAlternatingRowColors(True)
        self.table_widget_portfolio.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget_portfolio.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_portfolio.setSortingEnabled(True)
        self.table_widget_portfolio.setCornerButtonEnabled(False)
        self.table_widget_portfolio.horizontalHeader().setVisible(True)
        self.table_widget_portfolio.horizontalHeader().setCascadingSectionResizes(False)
        self.table_widget_portfolio.horizontalHeader().setStretchLastSection(False)
        self.table_widget_portfolio.verticalHeader().setVisible(False)
        self.table_widget_portfolio.verticalHeader().setCascadingSectionResizes(False)

        self.vert_layout_dialog.addWidget(self.table_widget_portfolio)

        self.vert_spacer_dialog = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vert_layout_dialog.addItem(self.vert_spacer_dialog)


        self.retranslateUi(dialog_transaction_history)

        QMetaObject.connectSlotsByName(dialog_transaction_history)
    # setupUi

    def retranslateUi(self, dialog_transaction_history):
        dialog_transaction_history.setWindowTitle(QCoreApplication.translate("dialog_transaction_history", u"Dialog", None))
        self.lbl_transaction_history.setText(QCoreApplication.translate("dialog_transaction_history", u"Transaction History", None))
        ___qtablewidgetitem = self.table_widget_portfolio.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("dialog_transaction_history", u"Transaction Type", None));
        ___qtablewidgetitem1 = self.table_widget_portfolio.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("dialog_transaction_history", u"Timestamp", None));
        ___qtablewidgetitem2 = self.table_widget_portfolio.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("dialog_transaction_history", u"Transaction ID", None));
        ___qtablewidgetitem3 = self.table_widget_portfolio.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("dialog_transaction_history", u"Symbol", None));
        ___qtablewidgetitem4 = self.table_widget_portfolio.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("dialog_transaction_history", u"Name", None));
        ___qtablewidgetitem5 = self.table_widget_portfolio.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("dialog_transaction_history", u"Platform", None));
        ___qtablewidgetitem6 = self.table_widget_portfolio.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("dialog_transaction_history", u"Units", None));
        ___qtablewidgetitem7 = self.table_widget_portfolio.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("dialog_transaction_history", u"Currency", None));
        ___qtablewidgetitem8 = self.table_widget_portfolio.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("dialog_transaction_history", u"Amount", None));
    # retranslateUi

