import PySide6.QtCore # Módulo para funcionalidades básicas de Qt
import PySide6.QtGui # Módulo para componentes gráficos
import PySide6.QtWidgets # Módulo para widgets de UI

class Ui_Widget(object):
    def setupUi(self, Widget):
        # Configuración inicial de la ventana principal
        Widget.resize(800, 600) # Establece tamaño inicial de la ventana (ancho, alto)
        Widget.setStyleSheet(u"background-color: #1f1f1f;") # Fondo oscuro para la ventana

        # Creación de acciones (items de menú)
        self.actionOpen = PySide6.QtGui.QAction(Widget) # Acción para abrir archivos
        self.actionOpen.setObjectName(u"actionOpen") # Identificador único para la acción

        self.actionExport = PySide6.QtGui.QAction(Widget) # Acción para exportar
        self.actionExport.setObjectName(u"actionExport")

        self.actionApply_Margin_to_All_Tabs = PySide6.QtGui.QAction(Widget) # Acción para márgenes
        self.actionApply_Margin_to_All_Tabs.setObjectName(u"actionApply_Margin_to_All_Tabs")
        self.actionApply_Margin_to_All_Tabs.setCheckable(True) # Convertir en toggle
        self.actionApply_Margin_to_All_Tabs.setChecked(True) # Activar por defecto

        self.actionAbout = PySide6.QtGui.QAction(Widget) # Acción para información
        self.actionAbout.setObjectName(u"actionAbout")

        # Configuración del layout principal (organización vertical)
        self.verticalLayout = PySide6.QtWidgets.QVBoxLayout(Widget) # Layout vertical
        self.verticalLayout.setSpacing(0) # Sin espacio entre widgets
        self.verticalLayout.setContentsMargins(0, 0, 0, 0) # Sin márgenes

        # Configuración de la barra de menú
        self.menuBar = PySide6.QtWidgets.QMenuBar(Widget) # Crear barra de menú
        self.menuBar.setMinimumSize(PySide6.QtCore.QSize(0, 20)) # Altura mínima
        self.menuBar.setMaximumSize(PySide6.QtCore.QSize(16777215, 20)) # Altura fija
        self.menuBar.setNativeMenuBar(False) # Usar menú de Qt, no del sistema
        # Estilo CSS para la barra de menú
        self.menuBar.setStyleSheet(u"""
            QMenuBar
            {
                background-color: #1f1f1f;
                color: white;
            }

            QMenuBar::item
            {
                padding: 2px 8px;
                background-color: transparent;
            }

            QMenuBar::item:selected
            {
                background-color: #404244;
            }

            QMenu
            {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
                padding: 0px;
            }

            QMenu::item
            {
                padding: 4px 24px 4px 24px;
                background-color: transparent;
            }

            QMenu::item:selected
            {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding-left: 23px;
            }
        """)

        # Menú Archivo (File)
        self.menuFile = PySide6.QtWidgets.QMenu(self.menuBar) # Crear menú File
        self.menuFile.setTitle(u"File") # Título del menú
        self.menuFile.addAction(self.actionOpen) # Añadir acción Abrir
        self.menuFile.addAction(self.actionExport) # Añadir acción Exportar

        # Menú Selección (Select)
        self.menuSelect = PySide6.QtWidgets.QMenu(self.menuBar) # Crear menú Select
        self.menuSelect.setTitle(u"Select") # Título del menú
        # Estilo específico para este menú
        self.menuSelect.setStyleSheet(u"""
            QMenu
            {
                background-color: #292a2b;
                color: white;
                border: 1px solid #1b1b1b;
            }

            QMenu::item
            {
                padding: 4px 24px 4px 12px;
                background-color: transparent;
            }

            QMenu::item:selected
            {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding-left: 11px;
            }

            QMenu::indicator
            {
                width: 12px;
                height: 12px;
                background-color: #292a2b;
                border: 1px solid #505254;
                left: 4px;
            }

            QMenu::indicator:checked
            {
                background-color: #404244;
                border: 1px solid #505254;
            }
        """)
        self.menuSelect.addAction(self.actionApply_Margin_to_All_Tabs) # Añadir acción

        # Menú Ayuda (Help)
        self.menuHelp = PySide6.QtWidgets.QMenu(self.menuBar) # Crear menú Help
        self.menuHelp.setTitle(u"Help") # Título del menú
        self.menuHelp.addAction(self.actionAbout) # Añadir acción Acerca de

        # Añadir menús a la barra de menú
        self.menuBar.addAction(self.menuFile.menuAction()) # Añadir menú File
        self.menuBar.addAction(self.menuSelect.menuAction()) # Añadir menú Select
        self.menuBar.addAction(self.menuHelp.menuAction()) # Añadir menú Help

        self.verticalLayout.addWidget(self.menuBar) # Añadir barra de menú al layout

        # Configuración de la barra de pestañas
        self.tabBar = PySide6.QtWidgets.QTabBar(Widget) # Crear barra de pestañas
        self.tabBar.setMinimumSize(PySide6.QtCore.QSize(0, 24)) # Altura mínima
        self.tabBar.setMaximumSize(PySide6.QtCore.QSize(16777215, 24)) # Altura fija
        self.tabBar.setTabsClosable(True) # Mostrar botón para cerrar pestañas
        self.tabBar.setMovable(True) # Permitir reordenar pestañas
        # Estilo para la barra de pestañas
        self.tabBar.setStyleSheet(u"""
            QTabBar
            {
                background: #292a2b;
                border: none;
            }

            QTabBar::tab
            {
                background: #292a2b;
                color: white;
                min-width: 60px;
                padding: 3px 6px 3px 12px;
                border: 1px solid #1b1b1b;
                margin-right: 2px;
            }

            QTabBar::tab:selected
            {
                background: #235c96;
                border-bottom: 1px solid #50a0f0;
            }

            QTabBar::close-button
            {
                subcontrol-position: right;
                padding: 3px;
            }

            QTabBar::close-button:hover
            {
                background: #505254;
            }
        """)

        self.verticalLayout.addWidget(self.tabBar) # Añadir barra de pestañas al layout

        # Configuración del área central dividida (splitter)
        self.splitter = PySide6.QtWidgets.QSplitter(PySide6.QtCore.Qt.Horizontal) # Split horizontal
        self.splitter.setHandleWidth(4) # Ancho del divisor

        # Panel izquierdo (barra lateral)
        self.leftPanel = PySide6.QtWidgets.QWidget() # Widget para el panel
        self.leftPanel.setMinimumSize(PySide6.QtCore.QSize(16, 0)) # Ancho mínimo
        self.leftPanel.setMaximumSize(PySide6.QtCore.QSize(16, 16777215)) # Ancho fijo
        self.leftPanel.setStyleSheet(u"background-color: #292a2b;") # Color de fondo

        # Marcadores decorativos en el panel izquierdo
        self.label_1 = PySide6.QtWidgets.QLabel(self.leftPanel) # Primer marcador
        self.label_1.setGeometry(PySide6.QtCore.QRect(0, 0, 16, 6)) # Posición y tamaño
        self.label_1.setStyleSheet(u"background-color: #235c96; border: none;") # Estilo

        self.label_2 = PySide6.QtWidgets.QLabel(self.leftPanel) # Segundo marcador
        self.label_2.setGeometry(PySide6.QtCore.QRect(0, 0, 16, 6)) # Posición y tamaño
        self.label_2.setStyleSheet(u"background-color: #235c96; border: none;") # Estilo

        self.splitter.addWidget(self.leftPanel) # Añadir panel izquierdo al splitter

        # Visor PDF (área central)
        self.pdfView = PySide6.QtWidgets.QGraphicsView() # Crear visor PDF
        self.pdfView.setStyleSheet(u"background-color: #1f1f1f; border: none;") # Estilo
        self.pdfView.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Ocultar scroll horizontal
        self.pdfView.setAlignment(PySide6.QtCore.Qt.AlignCenter) # Centrar contenido

        self.splitter.addWidget(self.pdfView) # Añadir visor PDF al splitter

        # Scroll vertical (barra derecha)
        self.verticalScrollBar = PySide6.QtWidgets.QScrollBar() # Crear scrollbar
        self.verticalScrollBar.setOrientation(PySide6.QtCore.Qt.Vertical) # Orientación vertical
        self.verticalScrollBar.setMinimumSize(PySide6.QtCore.QSize(16, 0)) # Ancho mínimo
        self.verticalScrollBar.setMaximumSize(PySide6.QtCore.QSize(16, 16777215)) # Ancho fijo
        self.verticalScrollBar.setVisible(False) # Ocultar inicialmente
        # Estilo para la scrollbar
        self.verticalScrollBar.setStyleSheet(u"""
            QScrollBar
            {
                background: #292a2b;
                width: 16px;
            }

            QScrollBar::handle
            {
                background: #404244;
                min-height: 20px;
            }

            QScrollBar::handle:hover
            {
                background: #505254;
            }

            QScrollBar::add-page, QScrollBar::sub-page
            {
                background: #292a2b;
            }
        """)

        self.splitter.addWidget(self.verticalScrollBar) # Añadir scrollbar al splitter
        self.verticalLayout.addWidget(self.splitter) # Añadir splitter al layout principal

        self.retranslateUi(Widget) # Configurar textos traducibles
        PySide6.QtCore.QMetaObject.connectSlotsByName(Widget) # Conectar slots automáticamente

    def retranslateUi(self, Widget):
        # Configuración de todos los textos traducibles
        Widget.setWindowTitle(PySide6.QtCore.QCoreApplication.translate("Widget", u"Exakova TextFlow", None))
        self.actionOpen.setText(PySide6.QtCore.QCoreApplication.translate("Widget", u"Open", None))
        self.actionExport.setText(PySide6.QtCore.QCoreApplication.translate("Widget", u"Export", None))
        self.actionApply_Margin_to_All_Tabs.setText(PySide6.QtCore.QCoreApplication.translate("Widget", u"Apply Margin to All Tabs", None))
        self.actionAbout.setText(PySide6.QtCore.QCoreApplication.translate("Widget", u"About Exakova TextFlow", None))
        self.menuFile.setTitle(PySide6.QtCore.QCoreApplication.translate("Widget", u"File", None))
        self.menuSelect.setTitle(PySide6.QtCore.QCoreApplication.translate("Widget", u"Select", None))
        self.menuHelp.setTitle(PySide6.QtCore.QCoreApplication.translate("Widget", u"Help", None))

# Punto de entrada principal
if __name__ == "__main__":
    import sys
    app = PySide6.QtWidgets.QApplication(sys.argv) # Crear aplicación Qt
    widget = PySide6.QtWidgets.QWidget() # Crear widget principal
    ui = Ui_Widget() # Crear instancia de la interfaz
    ui.setupUi(widget) # Configurar la interfaz
    widget.show() # Mostrar la ventana
    sys.exit(app.exec()) # Ejecutar el bucle principal
