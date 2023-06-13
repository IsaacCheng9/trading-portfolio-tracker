# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1000, 600)
        font = QFont()
        font.setPointSize(12)
        main_window.setFont(font)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayoutWidget = QWidget(self.central_widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 981, 581))
        self.vert_layout_window = QVBoxLayout(self.verticalLayoutWidget)
        self.vert_layout_window.setObjectName(u"vert_layout_window")
        self.vert_layout_window.setContentsMargins(0, 0, 0, 0)
        self.lbl_app_header = QLabel(self.verticalLayoutWidget)
        self.lbl_app_header.setObjectName(u"lbl_app_header")
        font1 = QFont()
        font1.setPointSize(24)
        self.lbl_app_header.setFont(font1)

        self.vert_layout_window.addWidget(self.lbl_app_header)

        self.hori_line_header = QFrame(self.verticalLayoutWidget)
        self.hori_line_header.setObjectName(u"hori_line_header")
        self.hori_line_header.setFrameShape(QFrame.HLine)
        self.hori_line_header.setFrameShadow(QFrame.Sunken)

        self.vert_layout_window.addWidget(self.hori_line_header)

        self.hori_layout_btns = QHBoxLayout()
        self.hori_layout_btns.setObjectName(u"hori_layout_btns")
        self.btn_add_transaction = QPushButton(self.verticalLayoutWidget)
        self.btn_add_transaction.setObjectName(u"btn_add_transaction")
        self.btn_add_transaction.setFont(font)

        self.hori_layout_btns.addWidget(self.btn_add_transaction)

        self.btn_view_transactions = QPushButton(self.verticalLayoutWidget)
        self.btn_view_transactions.setObjectName(u"btn_view_transactions")

        self.hori_layout_btns.addWidget(self.btn_view_transactions)

        self.btn_view_portfolio_perf = QPushButton(self.verticalLayoutWidget)
        self.btn_view_portfolio_perf.setObjectName(u"btn_view_portfolio_perf")
        self.btn_view_portfolio_perf.setFont(font)

        self.hori_layout_btns.addWidget(self.btn_view_portfolio_perf)

        self.hori_spacer_btns = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hori_layout_btns.addItem(self.hori_spacer_btns)


        self.vert_layout_window.addLayout(self.hori_layout_btns)

        self.hori_line_buttons = QFrame(self.verticalLayoutWidget)
        self.hori_line_buttons.setObjectName(u"hori_line_buttons")
        self.hori_line_buttons.setFrameShape(QFrame.HLine)
        self.hori_line_buttons.setFrameShadow(QFrame.Sunken)

        self.vert_layout_window.addWidget(self.hori_line_buttons)

        self.lbl_last_updated = QLabel(self.verticalLayoutWidget)
        self.lbl_last_updated.setObjectName(u"lbl_last_updated")

        self.vert_layout_window.addWidget(self.lbl_last_updated)

        self.table_widget_portfolio = QTableWidget(self.verticalLayoutWidget)
        if (self.table_widget_portfolio.columnCount() < 8):
            self.table_widget_portfolio.setColumnCount(8)
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
        if (self.table_widget_portfolio.rowCount() < 1):
            self.table_widget_portfolio.setRowCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_widget_portfolio.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_widget_portfolio.setItem(0, 7, __qtablewidgetitem16)
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

        self.vert_layout_window.addWidget(self.table_widget_portfolio)

        self.vert_spacer_app = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vert_layout_window.addItem(self.vert_spacer_app)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Trading Portfolio Tracker", None))
        self.lbl_app_header.setText(QCoreApplication.translate("main_window", u"Trading Portfolio Tracker", None))
        self.btn_add_transaction.setText(QCoreApplication.translate("main_window", u"Add Transaction (Buy/Sell)", None))
        self.btn_view_transactions.setText(QCoreApplication.translate("main_window", u"View Transactions", None))
        self.btn_view_portfolio_perf.setText(QCoreApplication.translate("main_window", u"View Portfolio Performance", None))
        self.lbl_last_updated.setText(QCoreApplication.translate("main_window", u"Last Updated: DD/MM/YYYY HH:MM:SS", None))
        ___qtablewidgetitem = self.table_widget_portfolio.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("main_window", u"Ticker", None));
        ___qtablewidgetitem1 = self.table_widget_portfolio.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("main_window", u"Security", None));
        ___qtablewidgetitem2 = self.table_widget_portfolio.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("main_window", u"Weight", None));
        ___qtablewidgetitem3 = self.table_widget_portfolio.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("main_window", u"Units", None));
        ___qtablewidgetitem4 = self.table_widget_portfolio.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("main_window", u"Currency", None));
        ___qtablewidgetitem5 = self.table_widget_portfolio.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("main_window", u"Current Value", None));
        ___qtablewidgetitem6 = self.table_widget_portfolio.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("main_window", u"Change", None));
        ___qtablewidgetitem7 = self.table_widget_portfolio.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("main_window", u"Rate of Return (Absolute)", None));
        ___qtablewidgetitem8 = self.table_widget_portfolio.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("main_window", u"New Row", None));

        __sortingEnabled = self.table_widget_portfolio.isSortingEnabled()
        self.table_widget_portfolio.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.table_widget_portfolio.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("main_window", u"VUSA", None));
        ___qtablewidgetitem10 = self.table_widget_portfolio.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("main_window", u"Vanguard S&P 500 UCITS ETF", None));
        ___qtablewidgetitem11 = self.table_widget_portfolio.item(0, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("main_window", u"100.000%", None));
        ___qtablewidgetitem12 = self.table_widget_portfolio.item(0, 3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("main_window", u"16.35783718", None));
        ___qtablewidgetitem13 = self.table_widget_portfolio.item(0, 4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("main_window", u"GBP", None));
        ___qtablewidgetitem14 = self.table_widget_portfolio.item(0, 5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("main_window", u"1000", None));
        ___qtablewidgetitem15 = self.table_widget_portfolio.item(0, 6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("main_window", u"1077", None));
        ___qtablewidgetitem16 = self.table_widget_portfolio.item(0, 7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("main_window", u"+7.7%", None));
        self.table_widget_portfolio.setSortingEnabled(__sortingEnabled)

    # retranslateUi

