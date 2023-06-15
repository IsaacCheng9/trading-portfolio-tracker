# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_transaction.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_dialog_add_transaction(object):
    def setupUi(self, dialog_add_transaction):
        if not dialog_add_transaction.objectName():
            dialog_add_transaction.setObjectName("dialog_add_transaction")
        dialog_add_transaction.resize(400, 375)
        font = QFont()
        font.setPointSize(12)
        dialog_add_transaction.setFont(font)
        self.verticalLayoutWidget = QWidget(dialog_add_transaction)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 381, 357))
        self.vert_layout_dialog = QVBoxLayout(self.verticalLayoutWidget)
        self.vert_layout_dialog.setObjectName("vert_layout_dialog")
        self.vert_layout_dialog.setContentsMargins(0, 0, 0, 0)
        self.lbl_add_transaction = QLabel(self.verticalLayoutWidget)
        self.lbl_add_transaction.setObjectName("lbl_add_transaction")
        font1 = QFont()
        font1.setPointSize(22)
        self.lbl_add_transaction.setFont(font1)

        self.vert_layout_dialog.addWidget(self.lbl_add_transaction)

        self.hori_line_transaction_header = QFrame(self.verticalLayoutWidget)
        self.hori_line_transaction_header.setObjectName("hori_line_transaction_header")
        self.hori_line_transaction_header.setFrameShape(QFrame.HLine)
        self.hori_line_transaction_header.setFrameShadow(QFrame.Sunken)

        self.vert_layout_dialog.addWidget(self.hori_line_transaction_header)

        self.form_layout_transaction = QFormLayout()
        self.form_layout_transaction.setObjectName("form_layout_transaction")
        self.lbl_transaction_type = QLabel(self.verticalLayoutWidget)
        self.lbl_transaction_type.setObjectName("lbl_transaction_type")

        self.form_layout_transaction.setWidget(
            0, QFormLayout.LabelRole, self.lbl_transaction_type
        )

        self.combo_box_transaction_type = QComboBox(self.verticalLayoutWidget)
        self.combo_box_transaction_type.addItem("")
        self.combo_box_transaction_type.addItem("")
        self.combo_box_transaction_type.setObjectName("combo_box_transaction_type")

        self.form_layout_transaction.setWidget(
            0, QFormLayout.FieldRole, self.combo_box_transaction_type
        )

        self.lbl_timestamp = QLabel(self.verticalLayoutWidget)
        self.lbl_timestamp.setObjectName("lbl_timestamp")

        self.form_layout_transaction.setWidget(
            1, QFormLayout.LabelRole, self.lbl_timestamp
        )

        self.datetime_edit_transaction = QDateTimeEdit(self.verticalLayoutWidget)
        self.datetime_edit_transaction.setObjectName("datetime_edit_transaction")
        self.datetime_edit_transaction.setTimeSpec(Qt.LocalTime)

        self.form_layout_transaction.setWidget(
            1, QFormLayout.FieldRole, self.datetime_edit_transaction
        )

        self.lbl_ticker = QLabel(self.verticalLayoutWidget)
        self.lbl_ticker.setObjectName("lbl_ticker")

        self.form_layout_transaction.setWidget(
            2, QFormLayout.LabelRole, self.lbl_ticker
        )

        self.line_edit_ticker = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_ticker.setObjectName("line_edit_ticker")

        self.form_layout_transaction.setWidget(
            2, QFormLayout.FieldRole, self.line_edit_ticker
        )

        self.lbl_platform = QLabel(self.verticalLayoutWidget)
        self.lbl_platform.setObjectName("lbl_platform")

        self.form_layout_transaction.setWidget(
            3, QFormLayout.LabelRole, self.lbl_platform
        )

        self.line_edit_platform = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_platform.setObjectName("line_edit_platform")

        self.form_layout_transaction.setWidget(
            3, QFormLayout.FieldRole, self.line_edit_platform
        )

        self.lbl_currency = QLabel(self.verticalLayoutWidget)
        self.lbl_currency.setObjectName("lbl_currency")

        self.form_layout_transaction.setWidget(
            4, QFormLayout.LabelRole, self.lbl_currency
        )

        self.line_edit_currency = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_currency.setObjectName("line_edit_currency")

        self.form_layout_transaction.setWidget(
            4, QFormLayout.FieldRole, self.line_edit_currency
        )

        self.lbl_amount = QLabel(self.verticalLayoutWidget)
        self.lbl_amount.setObjectName("lbl_amount")

        self.form_layout_transaction.setWidget(
            5, QFormLayout.LabelRole, self.lbl_amount
        )

        self.line_edit_amount = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_amount.setObjectName("line_edit_amount")

        self.form_layout_transaction.setWidget(
            5, QFormLayout.FieldRole, self.line_edit_amount
        )

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")

        self.form_layout_transaction.setWidget(6, QFormLayout.LabelRole, self.label)

        self.line_edit_unit_price = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_unit_price.setObjectName("line_edit_unit_price")

        self.form_layout_transaction.setWidget(
            6, QFormLayout.FieldRole, self.line_edit_unit_price
        )

        self.vert_layout_dialog.addLayout(self.form_layout_transaction)

        self.hori_line_transaction_form = QFrame(self.verticalLayoutWidget)
        self.hori_line_transaction_form.setObjectName("hori_line_transaction_form")
        self.hori_line_transaction_form.setFrameShape(QFrame.HLine)
        self.hori_line_transaction_form.setFrameShadow(QFrame.Sunken)

        self.vert_layout_dialog.addWidget(self.hori_line_transaction_form)

        self.lbl_status_msg = QLabel(self.verticalLayoutWidget)
        self.lbl_status_msg.setObjectName("lbl_status_msg")

        self.vert_layout_dialog.addWidget(self.lbl_status_msg)

        self.hori_layout_submit_transaction = QHBoxLayout()
        self.hori_layout_submit_transaction.setObjectName(
            "hori_layout_submit_transaction"
        )
        self.btn_submit_transaction = QPushButton(self.verticalLayoutWidget)
        self.btn_submit_transaction.setObjectName("btn_submit_transaction")

        self.hori_layout_submit_transaction.addWidget(self.btn_submit_transaction)

        self.btn_cancel_transaction = QPushButton(self.verticalLayoutWidget)
        self.btn_cancel_transaction.setObjectName("btn_cancel_transaction")

        self.hori_layout_submit_transaction.addWidget(self.btn_cancel_transaction)

        self.hori_spacer_btns = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.hori_layout_submit_transaction.addItem(self.hori_spacer_btns)

        self.vert_layout_dialog.addLayout(self.hori_layout_submit_transaction)

        self.vert_spacer_dialog = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.vert_layout_dialog.addItem(self.vert_spacer_dialog)

        self.retranslateUi(dialog_add_transaction)

        QMetaObject.connectSlotsByName(dialog_add_transaction)

    # setupUi

    def retranslateUi(self, dialog_add_transaction):
        dialog_add_transaction.setWindowTitle(
            QCoreApplication.translate(
                "dialog_add_transaction",
                "Add a Transaction \u2013 Trading Portfolio Tracker",
                None,
            )
        )
        self.lbl_add_transaction.setText(
            QCoreApplication.translate(
                "dialog_add_transaction", "Add a Transaction", None
            )
        )
        self.lbl_transaction_type.setText(
            QCoreApplication.translate(
                "dialog_add_transaction", "Transaction Type:", None
            )
        )
        self.combo_box_transaction_type.setItemText(
            0, QCoreApplication.translate("dialog_add_transaction", "Buy", None)
        )
        self.combo_box_transaction_type.setItemText(
            1, QCoreApplication.translate("dialog_add_transaction", "Sell", None)
        )

        self.lbl_timestamp.setText(
            QCoreApplication.translate("dialog_add_transaction", "Timestamp:", None)
        )
        self.lbl_ticker.setText(
            QCoreApplication.translate("dialog_add_transaction", "Ticker:", None)
        )
        self.lbl_platform.setText(
            QCoreApplication.translate("dialog_add_transaction", "Platform:", None)
        )
        self.lbl_currency.setText(
            QCoreApplication.translate("dialog_add_transaction", "Currency:", None)
        )
        self.lbl_amount.setText(
            QCoreApplication.translate("dialog_add_transaction", "Amount:", None)
        )
        self.label.setText(
            QCoreApplication.translate("dialog_add_transaction", "Unit Price:", None)
        )
        self.lbl_status_msg.setText(
            QCoreApplication.translate(
                "dialog_add_transaction",
                "Enter all the details of your transaction before submitting.",
                None,
            )
        )
        self.btn_submit_transaction.setText(
            QCoreApplication.translate("dialog_add_transaction", "Submit", None)
        )
        self.btn_cancel_transaction.setText(
            QCoreApplication.translate("dialog_add_transaction", "Cancel", None)
        )

    # retranslateUi
