# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/import.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(825, 726)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.group_deck_import = QtWidgets.QGroupBox(Dialog)
        self.group_deck_import.setObjectName("group_deck_import")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.group_deck_import)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cb_ignore_move_cards = QtWidgets.QCheckBox(self.group_deck_import)
        self.cb_ignore_move_cards.setObjectName("cb_ignore_move_cards")
        self.verticalLayout_5.addWidget(self.cb_ignore_move_cards)
        self.list_personal_fields = QtWidgets.QListWidget(self.group_deck_import)
        self.list_personal_fields.setObjectName("list_personal_fields")
        item = QtWidgets.QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.list_personal_fields.addItem(item)
        self.verticalLayout_5.addWidget(self.list_personal_fields)
        self.verticalLayout_2.addWidget(self.group_deck_import)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        Dialog.setWindowTitle(_translate("Dialog", "CrowdAnki Configuration"))
        self.group_deck_import.setTitle(_translate("Dialog", "Import"))
        self.cb_ignore_move_cards.setText(_translate("Dialog", "Do Not Move Existing Cards"))
        __sortingEnabled = self.list_personal_fields.isSortingEnabled()
        self.list_personal_fields.setSortingEnabled(False)
        item = self.list_personal_fields.item(0)
        item.setText(_translate("Dialog", "All Note Models"))
        self.list_personal_fields.setSortingEnabled(__sortingEnabled)
