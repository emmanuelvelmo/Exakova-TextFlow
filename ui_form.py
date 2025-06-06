# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QLabel, QMenu, QMenuBar, QSizePolicy,
    QSpacerItem, QSplitter, QTabBar, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        Widget.setStyleSheet(u"background-color: #1f1f1f;")
        self.actionOpen = QAction(Widget)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExport = QAction(Widget)
        self.actionExport.setObjectName(u"actionExport")
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.menuBar = QMenuBar(Widget)
        self.menuBar.setObjectName(u"menuBar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuBar.sizePolicy().hasHeightForWidth())
        self.menuBar.setSizePolicy(sizePolicy)
        self.menuBar.setMinimumSize(QSize(0, 24))
        self.menuBar.setStyleSheet(u"\n"
"            QMenuBar {\n"
"                background-color: #1f1f1f;\n"
"                color: white;\n"
"                border: none;\n"
"                padding: 2px 0px;\n"
"            }\n"
"            QMenuBar::item {\n"
"                padding: 2px 8px;\n"
"            }\n"
"            QMenuBar::item:selected {\n"
"                background-color: #404244;\n"
"            }\n"
"            QMenu {\n"
"                background-color: #292a2b;\n"
"                color: white;\n"
"                border: 1px solid #1b1b1b;\n"
"            }\n"
"            QMenu::item {\n"
"                padding: 4px 24px;\n"
"            }\n"
"            QMenu::item:selected {\n"
"                background-color: #235c96;\n"
"                border: 1px solid #50a0f0;\n"
"            }\n"
"          ")
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")

        self.verticalLayout.addWidget(self.menuBar)

        self.tabBar = QTabBar(Widget)
        self.tabBar.setObjectName(u"tabBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabBar.sizePolicy().hasHeightForWidth())
        self.tabBar.setSizePolicy(sizePolicy1)
        self.tabBar.setMinimumSize(QSize(0, 24))
        self.tabBar.setStyleSheet(u"\n"
"            QTabBar {\n"
"                background: #1f1f1f;\n"
"                border: none;\n"
"            }\n"
"            QTabBar::tab {\n"
"                background: #292a2b;\n"
"                color: white;\n"
"                min-width: 120px;\n"
"                padding: 3px 6px 3px 6px;\n"
"                border: 1px solid #1b1b1b;\n"
"                margin-right: 2px;\n"
"            }\n"
"            QTabBar::tab:selected {\n"
"                background: #235c96;\n"
"                border-bottom: 1px solid #50a0f0;\n"
"            }\n"
"          ")

        self.verticalLayout.addWidget(self.tabBar)

        self.splitter = QSplitter(Widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.leftPanel = QWidget(self.splitter)
        self.leftPanel.setObjectName(u"leftPanel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.leftPanel.sizePolicy().hasHeightForWidth())
        self.leftPanel.setSizePolicy(sizePolicy2)
        self.leftPanel.setMinimumSize(QSize(24, 0))
        self.leftPanel.setMaximumSize(QSize(24, 16777215))
        self.leftPanel.setStyleSheet(u"\n"
"              background-color: #292a2b;\n"
"              border-right: 1px solid #1b1b1b;\n"
"            ")
        self.verticalLayout_2 = QVBoxLayout(self.leftPanel)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.topSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.topSpacer)

        self.topMarginHandle = QFrame(self.leftPanel)
        self.topMarginHandle.setObjectName(u"topMarginHandle")
        self.topMarginHandle.setMinimumSize(QSize(24, 16))
        self.topMarginHandle.setMaximumSize(QSize(24, 16))
        self.topMarginHandle.setFrameShape(QFrame.StyledPanel)
        self.topMarginHandle.setStyleSheet(u"\n"
"                    QFrame {\n"
"                      background-color: #235c96;\n"
"                      border: 2px solid #50a0f0;\n"
"                      border-bottom: none;\n"
"                      border-radius: 4px 4px 0 0;\n"
"                    }\n"
"                    QFrame:hover {\n"
"                      background-color: #2a6db0;\n"
"                    }\n"
"                  ")
        self.horizontalLayout = QHBoxLayout(self.topMarginHandle)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.topHandleIcon = QLabel(self.topMarginHandle)
        self.topHandleIcon.setObjectName(u"topHandleIcon")
        self.topHandleIcon.setPixmap(QPixmap())
        self.topHandleIcon.setScaledContents(True)

        self.horizontalLayout.addWidget(self.topHandleIcon)


        self.verticalLayout_2.addWidget(self.topMarginHandle)

        self.selectionArea = QWidget(self.leftPanel)
        self.selectionArea.setObjectName(u"selectionArea")
        self.selectionArea.setStyleSheet(u"\n"
"                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                      stop:0 #1f1f1f, stop:0.5 #235c96, stop:1 #1f1f1f);\n"
"                    border-left: 2px solid #50a0f0;\n"
"                    border-right: 2px solid #50a0f0;\n"
"                  ")

        self.verticalLayout_2.addWidget(self.selectionArea)

        self.bottomMarginHandle = QFrame(self.leftPanel)
        self.bottomMarginHandle.setObjectName(u"bottomMarginHandle")
        self.bottomMarginHandle.setMinimumSize(QSize(24, 16))
        self.bottomMarginHandle.setMaximumSize(QSize(24, 16))
        self.bottomMarginHandle.setFrameShape(QFrame.StyledPanel)
        self.bottomMarginHandle.setStyleSheet(u"\n"
"                    QFrame {\n"
"                      background-color: #235c96;\n"
"                      border: 2px solid #50a0f0;\n"
"                      border-top: none;\n"
"                      border-radius: 0 0 4px 4px;\n"
"                    }\n"
"                    QFrame:hover {\n"
"                      background-color: #2a6db0;\n"
"                    }\n"
"                  ")
        self.horizontalLayout_2 = QHBoxLayout(self.bottomMarginHandle)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bottomHandleIcon = QLabel(self.bottomMarginHandle)
        self.bottomHandleIcon.setObjectName(u"bottomHandleIcon")
        self.bottomHandleIcon.setPixmap(QPixmap())
        self.bottomHandleIcon.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.bottomHandleIcon)


        self.verticalLayout_2.addWidget(self.bottomMarginHandle)

        self.bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.bottomSpacer)

        self.splitter.addWidget(self.leftPanel)
        self.pdfView = QGraphicsView(self.splitter)
        self.pdfView.setObjectName(u"pdfView")
        self.pdfView.setStyleSheet(u"\n"
"              background-color: white;\n"
"              border: none;\n"
"            ")
        self.splitter.addWidget(self.pdfView)

        self.verticalLayout.addWidget(self.splitter)


        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Exakova TextFlow", None))
        self.actionOpen.setText(QCoreApplication.translate("Widget", u"Open", None))
        self.actionExport.setText(QCoreApplication.translate("Widget", u"Export", None))
        self.menuFile.setTitle(QCoreApplication.translate("Widget", u"File", None))
    # retranslateUi