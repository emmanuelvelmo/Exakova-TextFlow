import PySide6.QtCore # Módulo para funcionalidades básicas de Qt
import PySide6.QtGui # Módulo para componentes gráficos
import PySide6.QtWidgets # Módulo para widgets de UI

# Clase principal para la interfaz de usuario
class Ui_Widget(object):
    def iniciar_ui(self, Widget):
        # Configuración de la ventana principal
        Widget.resize(800, 600) # Establece tamaño inicial de la ventana (ancho, alto)
        Widget.setStyleSheet(u"background-color: #1f1f1f;") # Fondo oscuro para la ventana
        Widget.setWindowTitle("Exakova TextFlow") # Texto del título de ventana

        # Configuración del layout principal (organización vertical)
        self.layout_vertical = PySide6.QtWidgets.QVBoxLayout(Widget) # Layout vertical
        self.layout_vertical.setSpacing(0) # Sin espacio entre widgets
        self.layout_vertical.setContentsMargins(0, 0, 0, 0) # Sin márgenes

        # Configuración de la barra de menú
        self.barra_menu = PySide6.QtWidgets.QMenuBar(Widget) # Crear barra de menú
        self.barra_menu.setMinimumSize(PySide6.QtCore.QSize(0, 20)) # Altura mínima
        self.barra_menu.setMaximumSize(PySide6.QtCore.QSize(16777215, 20)) # Altura fija
        self.barra_menu.setNativeMenuBar(False) # Usar menú de Qt, no del sistema
        self.barra_menu.setStyleSheet(u"""
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
        """) # Estilo CSS para la barra de menú

        # Creación de acciones (items de menú)
        self.accion_abrir = PySide6.QtGui.QAction(Widget) # Acción para abrir archivos
        self.accion_abrir.setText("Open") # Texto de la acción

        self.accion_exportar = PySide6.QtGui.QAction(Widget) # Acción para exportar
        self.accion_exportar.setText("Export") # Texto de la acción

        self.accion_aplicar_margen_todas_pestanas = PySide6.QtGui.QAction(Widget) # Acción para aplicar márgenes
        self.accion_aplicar_margen_todas_pestanas.setCheckable(True) # Convertir en toggle
        self.accion_aplicar_margen_todas_pestanas.setChecked(True) # Activar por defecto
        self.accion_aplicar_margen_todas_pestanas.setText("Apply Margins to All Tabs") # Texto de la acción

        self.accion_rango_paginas = PySide6.QtGui.QAction(Widget) # Acción para exportar
        self.accion_rango_paginas.setText("Pages Range") # Texto de la acción

        self.accion_acerca_de = PySide6.QtGui.QAction(Widget) # Acción para información
        self.accion_acerca_de.setText("About Exakova TextFlow") # Texto de la acción

        # Menú Archivo (File)
        self.menu_archivo = PySide6.QtWidgets.QMenu(self.barra_menu) # Crear menú Archivo
        self.menu_archivo.setTitle("File") # Título del menú

        self.menu_archivo.addAction(self.accion_abrir) # Añadir acción "Abrir"
        self.menu_archivo.addAction(self.accion_exportar) # Añadir acción "Exportar"

        # Menú Selección (Select)
        self.menu_seleccion = PySide6.QtWidgets.QMenu(self.barra_menu) # Crear menú Selección
        self.menu_seleccion.setTitle("Select") # Título del menú
        self.menu_seleccion.setStyleSheet(u"""
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
                border: 1px solid transparent;
            }

            QMenu::item:selected
            {
                background-color: #235c96;
                border: 1px solid #50a0f0;
                padding: 4px 24px 4px 12px;
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
                background-color: #2c73ba;
                border: 1px solid #505254;
            }
        """) # Estilo específico para este menú

        self.menu_seleccion.addAction(self.accion_aplicar_margen_todas_pestanas) # Añadir acción "Aplicar Margen a Todas las Pestañas"
        self.menu_seleccion.addAction(self.accion_rango_paginas) #

        # Menú Ayuda (Help)
        self.menu_ayuda = PySide6.QtWidgets.QMenu(self.barra_menu) # Crear menú Ayuda
        self.menu_ayuda.setTitle("Help") # Título del menú

        self.menu_ayuda.addAction(self.accion_acerca_de) # Añadir acción "Acerca de"

        # Añadir menús a la barra de menú
        self.barra_menu.addAction(self.menu_archivo.menuAction()) # Añadir menú "Archivo"
        self.barra_menu.addAction(self.menu_seleccion.menuAction()) # Añadir menú "Selección"
        self.barra_menu.addAction(self.menu_ayuda.menuAction()) # Añadir menú "Ayuda"

        self.layout_vertical.addWidget(self.barra_menu) # Añadir barra de menú al layout

        # Configuración de la barra de pestañas
        self.barra_pestanas = PySide6.QtWidgets.QTabBar(Widget) # Crear barra de pestañas
        self.barra_pestanas.setMinimumSize(PySide6.QtCore.QSize(0, 24)) # Altura mínima
        self.barra_pestanas.setMaximumSize(PySide6.QtCore.QSize(16777215, 24)) # Altura fija
        self.barra_pestanas.setTabsClosable(True) # Mostrar botón para cerrar pestañas
        self.barra_pestanas.setMovable(True) # Permitir reordenar pestañas
        # Estilo para la barra de pestañas
        self.barra_pestanas.setStyleSheet(u"""
            QTabBar
            {
                background: #292a2b;
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

        self.layout_vertical.addWidget(self.barra_pestanas) # Añadir barra de pestañas al layout

        # Configuración del área central con layout horizontal
        self.layout_horizontal = PySide6.QtWidgets.QHBoxLayout() # Layout horizontal
        self.layout_horizontal.setSpacing(0) # Sin espacio entre widgets
        self.layout_horizontal.setContentsMargins(0, 0, 0, 0) # Sin márgenes

        # Panel izquierdo (barra lateral)
        self.panel_izquierdo = PySide6.QtWidgets.QWidget() # Widget para el panel
        self.panel_izquierdo.setMinimumSize(PySide6.QtCore.QSize(16, 16)) # Ancho mínimo
        self.panel_izquierdo.setMaximumSize(PySide6.QtCore.QSize(16, 16777215)) # Ancho máximo
        self.panel_izquierdo.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Fixed, PySide6.QtWidgets.QSizePolicy.Expanding) # Política de tamaño
        self.panel_izquierdo.setStyleSheet(u"background-color: #292a2b;") # Color de fondo

        # Marcadores en el panel izquierdo
        self.etiqueta_1 = PySide6.QtWidgets.QLabel(self.panel_izquierdo) # Primer marcador
        self.etiqueta_1.setGeometry(PySide6.QtCore.QRect(0, 0, 16, 6)) # Posición y tamaño (arriba)
        self.etiqueta_1.setStyleSheet(u"background-color: #235c96; border: none;") # Estilo
        self.etiqueta_1.setCursor(PySide6.QtGui.QCursor(PySide6.QtCore.Qt.PointingHandCursor)) # Cursor personalizado

        self.etiqueta_2 = PySide6.QtWidgets.QLabel(self.panel_izquierdo) # Segundo marcador
        self.etiqueta_2.setGeometry(PySide6.QtCore.QRect(0, 6, 16, 6)) # Posición y tamaño (abajo)
        self.etiqueta_2.setStyleSheet(u"background-color: #235c96; border: none;") # Estilo
        self.etiqueta_2.setCursor(PySide6.QtGui.QCursor(PySide6.QtCore.Qt.PointingHandCursor)) # Cursor personalizado

        self.layout_horizontal.addWidget(self.panel_izquierdo) # Añadir panel izquierdo al layout

        # Visor PDF
        self.visor_pdf = PySide6.QtWidgets.QGraphicsView() # Crear visor PDF
        self.visor_pdf.setStyleSheet(u"""
            QGraphicsView
            {
                background-color: #1f1f1f;
                border: none;
            }
        """)

        self.visor_pdf.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Expanding) # Política de tamaño

        # Deshabilitar scrollbar por defecto
        self.visor_pdf.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff)
        self.visor_pdf.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff)

        self.layout_horizontal.addWidget(self.visor_pdf) # Añadir visor PDF a layout_horizontal

        # Panel derecho (barra lateral)
        self.panel_derecho = PySide6.QtWidgets.QWidget() # Widget para el panel
        self.panel_derecho.setMinimumSize(PySide6.QtCore.QSize(16, 16)) # Ancho mínimo
        self.panel_derecho.setMaximumSize(PySide6.QtCore.QSize(16, 16777215)) # Ancho máximo
        self.panel_derecho.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Fixed, PySide6.QtWidgets.QSizePolicy.Expanding) # Política de tamaño
        self.panel_derecho.setStyleSheet(u"background-color: #292a2b;") # Color de fondo

        # Etiqueta para panel derecho
        self.etiqueta_scroll = PySide6.QtWidgets.QLabel(self.panel_derecho) # Etiqueta que simula handler de una barra de desplazamiento
        self.etiqueta_scroll.setGeometry(PySide6.QtCore.QRect(0, 0, 16, 4)) # Posición y tamaño (arriba)
        self.etiqueta_scroll.setStyleSheet("""
            QLabel
            {
                background-color: #404244;
            }

            QLabel:hover
            {
                background-color: #505254;
            }
        """) # Estilo

        self.layout_horizontal.addWidget(self.panel_derecho) # Añadir panel derecho al layout

        # Áreas de selección de texto
        self.area_1 = PySide6.QtWidgets.QLabel(self.visor_pdf) # Primer área de selección
        self.area_1.setGeometry(PySide6.QtCore.QRect(0, 0, self.visor_pdf.width(), 6)) # Posición y tamaño (arriba)
        self.area_1.setStyleSheet(u"background-color: rgba(0, 0, 0, 40%); border: none;") # Negro con transparencia
        self.area_1.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Fixed) # Expandido horizontalmente, altura fija

        self.area_2 = PySide6.QtWidgets.QLabel(self.visor_pdf) # Segunda área de selección
        self.area_2.setGeometry(PySide6.QtCore.QRect(0, 6, self.visor_pdf.width(), 6)) # Posición y tamaño (6px desde arriba)
        self.area_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 40%); border: none;") # Negro con transparencia
        self.area_2.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Fixed) # Expandido horizontalmente, altura fija

        # Accesos directos con teclado
        self.shortcut_abrir = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("Ctrl + O"), Widget)
        self.shortcut_abrir.activated.connect(self.accion_abrir.trigger)

        self.shortcut_exportar = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("Ctrl + S"), Widget)
        self.shortcut_exportar.activated.connect(self.accion_exportar.trigger)

        # Crear un widget contenedor para el layout horizontal
        self.widget_central = PySide6.QtWidgets.QWidget() # Widget contenedor
        self.widget_central.setLayout(self.layout_horizontal) # Asignar el layout horizontal al contenedor

        self.layout_vertical.addWidget(self.widget_central) # Añadir contenedor al layout principal

        PySide6.QtCore.QMetaObject.connectSlotsByName(Widget) # Conectar slots automáticamente
