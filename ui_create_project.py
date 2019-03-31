# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_project.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateProject(object):
    def setupUi(self, CreateProject):
        CreateProject.setObjectName("CreateProject")
        CreateProject.resize(406, 187)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateProject)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(CreateProject)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edt_project_name = QtWidgets.QLineEdit(CreateProject)
        self.edt_project_name.setObjectName("edt_project_name")
        self.gridLayout.addWidget(self.edt_project_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(CreateProject)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.edt_website_path = QtWidgets.QLineEdit(CreateProject)
        self.edt_website_path.setObjectName("edt_website_path")
        self.gridLayout.addWidget(self.edt_website_path, 1, 1, 1, 1)
        self.btn_browse_website_path = QtWidgets.QPushButton(CreateProject)
        self.btn_browse_website_path.setObjectName("btn_browse_website_path")
        self.gridLayout.addWidget(self.btn_browse_website_path, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(CreateProject)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.edt_backup_path = QtWidgets.QLineEdit(CreateProject)
        self.edt_backup_path.setObjectName("edt_backup_path")
        self.gridLayout.addWidget(self.edt_backup_path, 2, 1, 1, 1)
        self.btn_browse_backup_path = QtWidgets.QPushButton(CreateProject)
        self.btn_browse_backup_path.setObjectName("btn_browse_backup_path")
        self.gridLayout.addWidget(self.btn_browse_backup_path, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(CreateProject)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.edt_work_path = QtWidgets.QLineEdit(CreateProject)
        self.edt_work_path.setObjectName("edt_work_path")
        self.gridLayout.addWidget(self.edt_work_path, 3, 1, 1, 1)
        self.btn_browse_work_path = QtWidgets.QPushButton(CreateProject)
        self.btn_browse_work_path.setObjectName("btn_browse_work_path")
        self.gridLayout.addWidget(self.btn_browse_work_path, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(CreateProject)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.edt_build_path = QtWidgets.QLineEdit(CreateProject)
        self.edt_build_path.setObjectName("edt_build_path")
        self.gridLayout.addWidget(self.edt_build_path, 4, 1, 1, 1)
        self.btn_browse_build_path = QtWidgets.QPushButton(CreateProject)
        self.btn_browse_build_path.setObjectName("btn_browse_build_path")
        self.gridLayout.addWidget(self.btn_browse_build_path, 4, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(CreateProject)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_cancel = QtWidgets.QPushButton(CreateProject)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CreateProject)
        QtCore.QMetaObject.connectSlotsByName(CreateProject)

    def retranslateUi(self, CreateProject):
        _translate = QtCore.QCoreApplication.translate
        CreateProject.setWindowTitle(_translate("CreateProject", "新建项目"))
        self.label.setText(_translate("CreateProject", "项目名："))
        self.label_2.setText(_translate("CreateProject", "网站路径："))
        self.btn_browse_website_path.setText(_translate("CreateProject", "浏览"))
        self.label_3.setText(_translate("CreateProject", "备份路径："))
        self.btn_browse_backup_path.setText(_translate("CreateProject", "浏览"))
        self.label_5.setText(_translate("CreateProject", "工作目录："))
        self.btn_browse_work_path.setText(_translate("CreateProject", "浏览"))
        self.label_4.setText(_translate("CreateProject", "生成目录："))
        self.btn_browse_build_path.setText(_translate("CreateProject", "浏览"))
        self.btn_ok.setText(_translate("CreateProject", "完成"))
        self.btn_cancel.setText(_translate("CreateProject", "取消"))


