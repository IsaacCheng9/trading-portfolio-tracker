# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'portfolio_performance.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_dialog_portfolio_perf(object):
    def setupUi(self, dialog_portfolio_perf):
        if not dialog_portfolio_perf.objectName():
            dialog_portfolio_perf.setObjectName(u"dialog_portfolio_perf")
        dialog_portfolio_perf.resize(800, 600)
        font = QFont()
        font.setPointSize(12)
        dialog_portfolio_perf.setFont(font)
        self.verticalLayoutWidget = QWidget(dialog_portfolio_perf)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 6, 781, 581))
        self.vert_layout_dialog = QVBoxLayout(self.verticalLayoutWidget)
        self.vert_layout_dialog.setObjectName(u"vert_layout_dialog")
        self.vert_layout_dialog.setContentsMargins(0, 0, 0, 0)
        self.lbl_portfolio_perf = QLabel(self.verticalLayoutWidget)
        self.lbl_portfolio_perf.setObjectName(u"lbl_portfolio_perf")
        font1 = QFont()
        font1.setPointSize(22)
        self.lbl_portfolio_perf.setFont(font1)

        self.vert_layout_dialog.addWidget(self.lbl_portfolio_perf)

        self.hori_line_portfolio_perf = QFrame(self.verticalLayoutWidget)
        self.hori_line_portfolio_perf.setObjectName(u"hori_line_portfolio_perf")
        self.hori_line_portfolio_perf.setFrameShape(QFrame.HLine)
        self.hori_line_portfolio_perf.setFrameShadow(QFrame.Sunken)

        self.vert_layout_dialog.addWidget(self.hori_line_portfolio_perf)

        self.lbl_last_updated = QLabel(self.verticalLayoutWidget)
        self.lbl_last_updated.setObjectName(u"lbl_last_updated")

        self.vert_layout_dialog.addWidget(self.lbl_last_updated)

        self.hori_line_last_updated = QFrame(self.verticalLayoutWidget)
        self.hori_line_last_updated.setObjectName(u"hori_line_last_updated")
        self.hori_line_last_updated.setFrameShape(QFrame.HLine)
        self.hori_line_last_updated.setFrameShadow(QFrame.Sunken)

        self.vert_layout_dialog.addWidget(self.hori_line_last_updated)

        self.lbl_returns_breakdown = QLabel(self.verticalLayoutWidget)
        self.lbl_returns_breakdown.setObjectName(u"lbl_returns_breakdown")
        font2 = QFont()
        font2.setPointSize(16)
        self.lbl_returns_breakdown.setFont(font2)

        self.vert_layout_dialog.addWidget(self.lbl_returns_breakdown)

        self.table_widget_returns_breakdown = QTableWidget(self.verticalLayoutWidget)
        if (self.table_widget_returns_breakdown.columnCount() < 3):
            self.table_widget_returns_breakdown.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_returns_breakdown.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.table_widget_returns_breakdown.rowCount() < 1):
            self.table_widget_returns_breakdown.setRowCount(1)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setItem(0, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setItem(0, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_returns_breakdown.setItem(0, 2, __qtablewidgetitem6)
        self.table_widget_returns_breakdown.setObjectName(u"table_widget_returns_breakdown")
        self.table_widget_returns_breakdown.setShowGrid(True)
        self.table_widget_returns_breakdown.setCornerButtonEnabled(False)
        self.table_widget_returns_breakdown.verticalHeader().setVisible(False)

        self.vert_layout_dialog.addWidget(self.table_widget_returns_breakdown)

        self.vert_spacer_dialog = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vert_layout_dialog.addItem(self.vert_spacer_dialog)


        self.retranslateUi(dialog_portfolio_perf)

        QMetaObject.connectSlotsByName(dialog_portfolio_perf)
    # setupUi

    def retranslateUi(self, dialog_portfolio_perf):
        dialog_portfolio_perf.setWindowTitle(QCoreApplication.translate("dialog_portfolio_perf", u"Trading Portfolio Tracker \u2013\u00a0Portfolio Performance Analysis", None))
        self.lbl_portfolio_perf.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Portfolio Performance Analysis", None))
        self.lbl_last_updated.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Last Updated: DD/MM/YYYY HH:MM:SS", None))
        self.lbl_returns_breakdown.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Breakdown of Returns", None))
        ___qtablewidgetitem = self.table_widget_returns_breakdown.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Rate of Return (Absolute)", None));
        ___qtablewidgetitem1 = self.table_widget_returns_breakdown.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Returns from Change of Value", None));
        ___qtablewidgetitem2 = self.table_widget_returns_breakdown.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Returns from Currency Risk", None));
        ___qtablewidgetitem3 = self.table_widget_returns_breakdown.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("dialog_portfolio_perf", u"Values", None));

        __sortingEnabled = self.table_widget_returns_breakdown.isSortingEnabled()
        self.table_widget_returns_breakdown.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.table_widget_returns_breakdown.item(0, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("dialog_portfolio_perf", u"N/A", None));
        ___qtablewidgetitem5 = self.table_widget_returns_breakdown.item(0, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("dialog_portfolio_perf", u"N/A", None));
        ___qtablewidgetitem6 = self.table_widget_returns_breakdown.item(0, 2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("dialog_portfolio_perf", u"N/A", None));
        self.table_widget_returns_breakdown.setSortingEnabled(__sortingEnabled)

    # retranslateUi

