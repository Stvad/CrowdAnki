# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/config.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(669, 651)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group_snapshot = QtWidgets.QGroupBox(Dialog)
        self.group_snapshot.setObjectName("group_snapshot")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_snapshot)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cb_automated_snapshot = QtWidgets.QCheckBox(self.group_snapshot)
        self.cb_automated_snapshot.setObjectName("cb_automated_snapshot")
        self.verticalLayout_3.addWidget(self.cb_automated_snapshot)
        self.lbl_snapshot = QtWidgets.QLabel(self.group_snapshot)
        self.lbl_snapshot.setObjectName("lbl_snapshot")
        self.verticalLayout_3.addWidget(self.lbl_snapshot)
        self.textedit_snapshot_root_decks = QtWidgets.QPlainTextEdit(self.group_snapshot)
        self.textedit_snapshot_root_decks.setObjectName("textedit_snapshot_root_decks")
        self.verticalLayout_3.addWidget(self.textedit_snapshot_root_decks)
        self.verticalLayout.addWidget(self.group_snapshot)
        self.group_deck_export = QtWidgets.QGroupBox(Dialog)
        self.group_deck_export.setObjectName("group_deck_export")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.group_deck_export)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lbl_deck_sort = QtWidgets.QLabel(self.group_deck_export)
        self.lbl_deck_sort.setObjectName("lbl_deck_sort")
        self.verticalLayout_4.addWidget(self.lbl_deck_sort)
        self.textedit_deck_sort_methods = QtWidgets.QPlainTextEdit(self.group_deck_export)
        self.textedit_deck_sort_methods.setObjectName("textedit_deck_sort_methods")
        self.verticalLayout_4.addWidget(self.textedit_deck_sort_methods)
        self.cb_reverse_sort = QtWidgets.QCheckBox(self.group_deck_export)
        self.cb_reverse_sort.setObjectName("cb_reverse_sort")
        self.verticalLayout_4.addWidget(self.cb_reverse_sort)
        self.verticalLayout.addWidget(self.group_deck_export)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.group_snapshot.setTitle(_translate("Dialog", "Snapshot Options"))
        self.cb_automated_snapshot.setText(_translate("Dialog", "Automated Snapshot"))
        self.lbl_snapshot.setText(_translate("Dialog", "Snapshot Root Decks (separated by comma)"))
        self.group_deck_export.setTitle(_translate("Dialog", "Deck Export Sorting Options"))
        self.lbl_deck_sort.setText(_translate("Dialog", "Deck Sort Method(s) (separated by comma)"))
        self.cb_reverse_sort.setText(_translate("Dialog", "Reverse Sort Order"))

