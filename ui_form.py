from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, QRect, Qt)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMenu, QMenuBar, QPushButton, QScrollBar, QSizePolicy, QSplitter, QTabBar,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        Widget.setStyleSheet(u"background-color: #1f1f1f;")

        # Actions
        self.actionOpen = QAction(Widget)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExport = QAction(Widget)
        self.actionExport.setObjectName(u"actionExport")
        self.actionApply_Margin_to_All_Tabs = QAction(Widget)
        self.actionApply_Margin_to_All_Tabs.setObjectName(u"actionApply_Margin_to_All_Tabs")
        self.actionApply_Margin_to_All_Tabs.setCheckable(True)
        self.actionApply_Margin_to_All_Tabs.setChecked(True)

        # Layout principal
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Menú
        self.menuBar = QMenuBar(Widget)
        self.menuBar.setMinimumSize(QSize(0, 24))
        self.menuBar.setMaximumSize(QSize(16777215, 24))
        self.menuBar.setStyleSheet(u"""
            QMenuBar {
                background-color: #1f1f1f;
                color: white;
                border: none;
                padding: 2px 0px;
            }
            QMenuBar::item {
                padding: 2px 8px;
            }
            QMenuBar::item:selected {
                background-color: #404244;
            }
            QMenu {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
            }
            QMenu::item {
                padding: 4px 24px;
            }
            QMenu::item:selected {
                background-color: #235c96;
                border: 1px solid #50a0f0;
            }
        """)
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setTitle(u"File")
        self.menuSelect = QMenu(self.menuBar)
        self.menuSelect.setTitle(u"Select")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)
        self.menuSelect.addAction(self.actionApply_Margin_to_All_Tabs)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSelect.menuAction())
        self.verticalLayout.addWidget(self.menuBar)

        # Layout horizontal de pestañas + botones
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)

        self.tabBar = QTabBar(Widget)
        self.tabBar.setMinimumSize(QSize(32, 24))
        self.tabBar.setMaximumSize(QSize(16777215, 24))
        self.tabBar.setStyleSheet(u"""
            QTabBar {
                background: #292a2b;
                border: none;
            }
            QTabBar::tab {
                background: #292a2b;
                color: white;
                min-width: 60px;
                padding: 3px 6px;
                border: 1px solid #1b1b1b;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #235c96;
                border-bottom: 1px solid #50a0f0;
            }
        """)

        self.pushButton_1 = QPushButton(u"+", Widget)
        self.pushButton_1.setMinimumSize(QSize(24, 24))
        self.pushButton_1.setMaximumSize(QSize(24, 24))
        self.pushButton_1.setStyleSheet(u"""
            QPushButton {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #404244;
            }
        """)

        self.pushButton_2 = QPushButton(u"-", Widget)
        self.pushButton_2.setMinimumSize(QSize(24, 24))
        self.pushButton_2.setMaximumSize(QSize(24, 24))
        self.pushButton_2.setStyleSheet(u"""
            QPushButton {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #404244;
            }
        """)

        self.horizontalLayout.addWidget(self.tabBar)
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Splitter central
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(4)

        # Panel izquierdo
        self.leftPanel = QWidget()
        self.leftPanel.setMinimumSize(QSize(16, 0))
        self.leftPanel.setMaximumSize(QSize(16, 16777215))
        self.leftPanel.setStyleSheet(u"background-color: #292a2b; border-right: 1px solid #1b1b1b;")

        self.label_1 = QLabel(u"\u25B6", self.leftPanel)
        self.label_1.setGeometry(QRect(0, 0, 16, 16))
        self.label_1.setStyleSheet(u"color: white; background-color: #235c96; border: 1px solid #50a0f0; border-radius: 2px;")

        self.label_2 = QLabel(u"\u25B6", self.leftPanel)
        self.label_2.setGeometry(QRect(0, 584, 16, 16))
        self.label_2.setStyleSheet(u"color: white; background-color: #235c96; border: 1px solid #50a0f0; border-radius: 2px;")

        self.splitter.addWidget(self.leftPanel)

        # Visor PDF
        self.pdfView = QGraphicsView()
        self.pdfView.setStyleSheet(u"background-color: #1f1f1f; border: none;")
        self.splitter.addWidget(self.pdfView)

        # Scroll vertical
        self.verticalScrollBar = QScrollBar()
        self.verticalScrollBar.setOrientation(Qt.Vertical)
        self.verticalScrollBar.setMinimumSize(QSize(16, 0))
        self.verticalScrollBar.setMaximumSize(QSize(16, 16777215))
        self.verticalScrollBar.setStyleSheet(u"""
            QScrollBar {
                background: #292a2b;
                width: 16px;
            }
            QScrollBar::handle {
                background: #404244;
                min-height: 20px;
            }
            QScrollBar::handle:hover {
                background: #505254;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
        """)
        self.splitter.addWidget(self.verticalScrollBar)

        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Exakova TextFlow", None))
        self.actionOpen.setText(QCoreApplication.translate("Widget", u"Open", None))
        self.actionExport.setText(QCoreApplication.translate("Widget", u"Export", None))
        self.actionApply_Margin_to_All_Tabs.setText(QCoreApplication.translate("Widget", u"Apply Margin to All Tabs", None))
