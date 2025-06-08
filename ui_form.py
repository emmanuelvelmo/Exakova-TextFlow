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
        self.menuBar.setNativeMenuBar(False)  # Esto es clave para evitar el comportamiento nativo
        self.menuBar.setStyleSheet(u"""
            /* Estilo del menú bar */
            QMenuBar {
                background-color: #1f1f1f;
                color: white;
            }

            /* Estilo del menú bar al pasar el cursor */
            QMenuBar::item {
                padding: 2px 8px;
                background-color: transparent;
                border-radius: 0px;
            }

            QMenuBar::item:selected {
                background-color: #404244;
            }

            /* Estilo de los submenús */
            QMenu {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
                padding: 0px;
            }

            /* Estilo de las acciones */
            QMenu::item {
                padding: 4px 24px 4px 24px;
                background-color: transparent;
            }

            /* Estilo de las acciones al pasar el cursor */
            QMenu::item:selected {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding: 4px 24px 4px 23px;
            }

            /* Estilo del indicador de checkbox */
            QMenu::indicator {
                width: 13px;
                height: 13px;
                left: 5px;
            }

            QMenu::indicator:unchecked {
                background-color: #292a2b;
                border: 1px solid #505254;
            }

            QMenu::indicator:checked {
                background-color: #292a2b;
                border: 1px solid #505254;
                image: url(:/qss_icons/rc/checkbox_checked.png);
            }

            QMenu::indicator:checked:disabled {
                image: url(:/qss_icons/rc/checkbox_checked_disabled.png);
            }

            /* Sombra para los submenús */
            QMenu {
                box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
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

        # Resto del código permanece igual...
        # TabBar
        self.tabBar = QTabBar(Widget)
        self.tabBar.setObjectName(u"tabBar")
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
        self.splitter.setObjectName(u"splitter")
        self.splitter.setHandleWidth(4)

        # Panel izquierdo (16px de ancho)
        self.leftPanel = QWidget()
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftPanel.setMinimumSize(QSize(16, 0))
        self.leftPanel.setMaximumSize(QSize(16, 16777215))
        self.leftPanel.setStyleSheet(u"background-color: #292a2b;")

        # Label 1 (rectángulo azul 16x8)
        self.label_1 = QLabel(self.leftPanel)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setGeometry(QRect(0, 0, 16, 6))
        self.label_1.setStyleSheet(u"""
            background-color: #235c96;
            border: none;
        """)

        # Label 2 (rectángulo azul 16x8)
        self.label_2 = QLabel(self.leftPanel)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 584, 16, 6))
        self.label_2.setStyleSheet(u"""
            background-color: #235c96;
            border: none;
        """)

        self.splitter.addWidget(self.leftPanel)

        # Visor PDF (sin scroll horizontal)
        self.pdfView = QGraphicsView()
        self.pdfView.setObjectName(u"pdfView")
        self.pdfView.setStyleSheet(u"background-color: #1f1f1f; border: none;")
        self.pdfView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pdfView.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.pdfView)

        # Scroll vertical (inicialmente oculto)
        self.verticalScrollBar = QScrollBar()
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
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
