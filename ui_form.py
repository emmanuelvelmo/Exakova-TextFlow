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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QMenu, QMenuBar,
    QScrollBar, QSizePolicy, QSplitter, QTabBar,
    QVBoxLayout, QWidget)

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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
        sizePolicy.setHeightForWidth(self.tabBar.sizePolicy().hasHeightForWidth())
        self.tabBar.setSizePolicy(sizePolicy)
        self.tabBar.setMinimumSize(QSize(0, 24))
        self.tabBar.setStyleSheet(u"\n"
"            QTabBar {\n"
"                background: #292a2b;\n"
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
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(4)
        self.leftPanel = QWidget(self.splitter)
        self.leftPanel.setObjectName(u"leftPanel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.leftPanel.sizePolicy().hasHeightForWidth())
        self.leftPanel.setSizePolicy(sizePolicy1)
        self.leftPanel.setMinimumSize(QSize(16, 0))
        self.leftPanel.setMaximumSize(QSize(16, 16777215))
        self.leftPanel.setStyleSheet(u"\n"
"              background-color: #292a2b;\n"
"              border-right: 1px solid #1b1b1b;\n"
"            ")
        self.splitter.addWidget(self.leftPanel)
        self.pdfView = QGraphicsView(self.splitter)
        self.pdfView.setObjectName(u"pdfView")
        self.pdfView.setStyleSheet(u"\n"
"              background-color: #1f1f1f;\n"
"              border: none;\n"
"            ")
        self.splitter.addWidget(self.pdfView)
        self.rightScrollBar = QScrollBar(self.splitter)
        self.rightScrollBar.setObjectName(u"rightScrollBar")
        sizePolicy1.setHeightForWidth(self.rightScrollBar.sizePolicy().hasHeightForWidth())
        self.rightScrollBar.setSizePolicy(sizePolicy1)
        self.rightScrollBar.setMinimumSize(QSize(16, 0))
        self.rightScrollBar.setMaximumSize(QSize(16, 16777215))
        self.rightScrollBar.setStyleSheet(u"\n"
"              QScrollBar {\n"
"                  background: #292a2b;\n"
"                  width: 16px;\n"
"              }\n"
"              QScrollBar::handle {\n"
"                  background: #404244;\n"
"                  min-height: 20px;\n"
"              }\n"
"              QScrollBar::handle:hover {\n"
"                  background: #505254;\n"
"              }\n"
"              QScrollBar::add-line, QScrollBar::sub-line {\n"
"                  background: none;\n"
"              }\n"
"            ")
        self.rightScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.rightScrollBar)

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

