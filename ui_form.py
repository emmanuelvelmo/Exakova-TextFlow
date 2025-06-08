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

        # Menú con estilo mejorado
        self.menuBar = QMenuBar(Widget)
        self.menuBar.setMinimumSize(QSize(0, 20))
        self.menuBar.setMaximumSize(QSize(16777215, 20))
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.setStyleSheet(u"""
            QMenuBar {
                background-color: #1f1f1f;
                color: white;
            }

            QMenuBar::item {
                padding: 2px 8px;
                background-color: transparent;
            }

            QMenuBar::item:selected {
                background-color: #404244;
            }

            QMenu {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
                padding: 0px;
            }

            QMenu::item {
                padding: 4px 24px 4px 24px;
                background-color: transparent;
            }

            QMenu::item:selected {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding-left: 23px;
            }
        """)

        # Menú File
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setTitle(u"File")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)

        # Menú Select
        self.menuSelect = QMenu(self.menuBar)
        self.menuSelect.setTitle(u"Select")
        self.menuSelect.setStyleSheet(u"""
            QMenu {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
            }

            QMenu::item {
                padding: 4px 24px 4px 12px;
                background-color: transparent;
            }

            QMenu::item:selected {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding-left: 11px;
            }

            QMenu::indicator {
                width: 12px;
                height: 12px;
                background-color: #292a2b;
                border: 1px solid #505254;
                left: 4px;
            }

            QMenu::indicator:checked {
                background-color: #404244;
                border: 1px solid #505254;
            }
        """)

        self.menuSelect.addAction(self.actionApply_Margin_to_All_Tabs)

        # Añadir a la barra
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSelect.menuAction())
        self.verticalLayout.addWidget(self.menuBar)

        # TabBar
        self.tabBar = QTabBar(Widget)
        self.tabBar.setMinimumSize(QSize(0, 24))
        self.tabBar.setMaximumSize(QSize(16777215, 24))
        self.tabBar.setTabsClosable(True)
        self.tabBar.setMovable(True)
        self.tabBar.setStyleSheet(u"""
            QTabBar {
                background: #292a2b;
                border: none;
            }
            QTabBar::tab {
                background: #292a2b;
                color: white;
                min-width: 60px;
                padding: 3px 6px 3px 12px;
                border: 1px solid #1b1b1b;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #235c96;
                border-bottom: 1px solid #50a0f0;
            }
            QTabBar::close-button {
                subcontrol-position: right;
                padding: 3px;
                image: none;
            }
            QTabBar::close-button:hover {
                background: #505254;
            }
        """)
        self.verticalLayout.addWidget(self.tabBar)

        # Splitter central
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(4)

        # Panel izquierdo
        self.leftPanel = QWidget()
        self.leftPanel.setMinimumSize(QSize(16, 0))
        self.leftPanel.setMaximumSize(QSize(16, 16777215))
        self.leftPanel.setStyleSheet(u"background-color: #292a2b;")

        self.label_1 = QLabel(self.leftPanel)
        self.label_1.setGeometry(QRect(0, 0, 16, 6))
        self.label_1.setStyleSheet(u"background-color: #235c96; border: none;")

        self.label_2 = QLabel(self.leftPanel)
        self.label_2.setGeometry(QRect(0, 584, 16, 6))
        self.label_2.setStyleSheet(u"background-color: #235c96; border: none;")

        self.splitter.addWidget(self.leftPanel)

        # Visor PDF
        self.pdfView = QGraphicsView()
        self.pdfView.setStyleSheet(u"background-color: #1f1f1f; border: none;")
        self.pdfView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pdfView.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.pdfView)

        # Scroll vertical
        self.verticalScrollBar = QScrollBar()
        self.verticalScrollBar.setOrientation(Qt.Vertical)
        self.verticalScrollBar.setMinimumSize(QSize(16, 0))
        self.verticalScrollBar.setMaximumSize(QSize(16, 16777215))
        self.verticalScrollBar.setVisible(False)
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
                border: none;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: #292a2b;
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
        self.menuFile.setTitle(QCoreApplication.translate("Widget", u"File", None))
        self.menuSelect.setTitle(QCoreApplication.translate("Widget", u"Select", None))


# Lanzador
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = QWidget()
    ui = Ui_Widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec())
