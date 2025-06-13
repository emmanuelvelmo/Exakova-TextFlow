import sys # Módulo para funciones del sistema
import os # Módulo para operaciones del sistema operativo
import PySide6.QtWidgets # Módulo para widgets de UI
import PySide6.QtGui # Módulo para componentes gráficos
import PySide6.QtCore # Módulo para funcionalidades básicas de Qt
import fitz # Librería PyMuPDF para manejo de archivos PDF
import ui_form # Módulo con la interfaz de usuario generada

# CONFIGURACIÓN DE LA APLICACIÓN
app = PySide6.QtWidgets.QApplication(sys.argv) # Crea la aplicación Qt

if hasattr(sys, 'frozen'): # Si la aplicación está compilada (ejecutable)
    os.environ["PATH"] += os.pathsep + PySide6.QtCore.QLibraryInfo.location(PySide6.QtCore.QLibraryInfo.BinariesPath) # Añade binarios Qt al PATH

# Crear el widget principal
vent_princ = PySide6.QtWidgets.QWidget() # Crea el widget principal de la aplicación

ui = ui_form.Ui_Widget() # Crea instancia de la interfaz de usuario
ui.setupUi(vent_princ) # Configura la interfaz en el widget principal

# CONFIGURACIÓN DE LA INTERFAZ DE USUARIO
# Configurar escena gráfica para PDF
scene = PySide6.QtWidgets.QGraphicsScene() # Crea nueva escena gráfica

ui.visor_pdf.setScene(scene) # Asigna la escena a la vista PDF
ui.visor_pdf.setRenderHints(PySide6.QtGui.QPainter.Antialiasing | PySide6.QtGui.QPainter.SmoothPixmapTransform | PySide6.QtGui.QPainter.TextAntialiasing) # Configura renderizado de alta calidad
ui.visor_pdf.setAlignment(PySide6.QtCore.Qt.AlignCenter) # Centra el contenido en la vista

# Configurar barras de desplazamiento
ui.visor_pdf.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Oculta scrollbar vertical interno
ui.visor_pdf.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Oculta scrollbar horizontal interno
ui.barra_desplazamiento_vertical.setVisible(False) # Inicialmente oculta la barra de desplazamiento externa

# Configurar estilos de la barra de tabs
tab_close_button_style = """
    Qbarra_pestanas::close-button
    {
        subcontrol-origin: padding;
        subcontrol-position: right;
        width: 16px;
        height: 16px;
        margin-right: 2px;
    }

    Qbarra_pestanas::close-button:hover
    {
        background: #505254;
        border-radius: 2px;
    }
""" # Estilos CSS para el botón de cierre de tabs

ui.barra_pestanas.setStyleSheet(ui.barra_pestanas.styleSheet() + tab_close_button_style) # Aplica los estilos al tab bar

# VARIABLES GLOBALES
current_file = None # Archivo PDF actualmente abierto
doc = None # Documento PDF actual
docs = {} # Diccionario que almacena todos los documentos abiertos por índice de tab
page_items = [] # Lista de elementos gráficos de páginas PDF
page_spacing = 10 # Espaciado entre páginas en píxeles

# FUNCIONES DE GESTIÓN DE INTERFAZ
# Maneja el cambio de pestaña en la interfaz
def cambiar_pestana(index):
    global doc, current_file # Declara variables globales que se modificarán

    if index >= 0 and index in docs: # Verifica que el índice sea válido y exista en docs
        doc = docs[index] # Cambia al documento del tab seleccionado
        current_file = doc.name # Actualiza el archivo actual
        mostrar_paginas_pdf() # Muestra las páginas del nuevo documento
        ajustar_barra_desplazamiento() # Ajusta la barra de desplazamiento
        centrar_primera_pagina() # Centra la primera página

# Cierra una pestaña abierta y gestiona los recursos asociados
def cerrar_pestana(index):
    global current_file, doc # Declara variables globales que se modificarán

    if index in docs: # Si el índice existe en docs
        docs[index].close() # Cierra el documento

        del docs[index] # Elimina el documento del diccionario

    ui.barra_pestanas.removeTab(index) # Remueve el tab de la barra

    if ui.barra_pestanas.count() == 0: # Si no quedan tabs abiertos
        limpiar_vista_pdf() # Limpia la vista PDF
        current_file = None # Reinicia el archivo actual
        doc = None # Reinicia el documento actual

# Sincroniza el desplazamiento vertical de la vista PDF con la barra de desplazamiento personalizada
def desplazar_vista_pdf(value):
    ui.visor_pdf.barra_desplazamiento_vertical().setValue(value) # Sincroniza el desplazamiento de la vista PDF

# Centra la primera página del documento en la vista
def centrar_primera_pagina():
    if not page_items: # Si no hay páginas cargadas
        return # Sale de la función

    PySide6.QtCore.QTimer.singleShot(50, lambda: ui.visor_pdf.fitInView(page_items[0], PySide6.QtCore.Qt.KeepAspectRatio)) # Centra la primera página después de 50ms manteniendo proporción

# Limpia la vista del PDF y reinicia los elementos relacionados
def limpiar_vista_pdf():
    global page_items # Declara variable global que se modificará

    scene.clear() # Limpia todos los elementos de la escena
    page_items = [] # Reinicia la lista de páginas
    ui.barra_desplazamiento_vertical.setVisible(False) # Oculta la barra de desplazamiento

# Ajusta la visibilidad y configuración de la barra de desplazamiento vertical
def ajustar_barra_desplazamiento():
    if not doc or not page_items: # Si no hay documento o páginas
        ui.barra_desplazamiento_vertical.setVisible(False) # Oculta la barra de desplazamiento

        return # Sale de la función

    view_height = ui.visor_pdf.viewport().height() # Obtiene altura del viewport
    content_height = scene.sceneRect().height() # Obtiene altura del contenido
    needs_scrollbar = content_height > view_height # Determina si necesita scrollbar

    ui.barra_desplazamiento_vertical.setVisible(needs_scrollbar) # Muestra/oculta scrollbar según necesidad

    if needs_scrollbar: # Si necesita scrollbar
        pdf_scrollbar = ui.visor_pdf.barra_desplazamiento_vertical() # Obtiene scrollbar interno
        ui.barra_desplazamiento_vertical.setRange(0, pdf_scrollbar.maximum()) # Establece rango del scrollbar externo
        ui.barra_desplazamiento_vertical.setPageStep(pdf_scrollbar.pageStep()) # Sincroniza paso de página
        ui.barra_desplazamiento_vertical.setSingleStep(pdf_scrollbar.singleStep()) # Sincroniza paso simple

        visible_ratio = view_height / content_height # Calcula proporción visible
        handle_size = max(20, int(ui.barra_desplazamiento_vertical.height() * visible_ratio)) # Calcula tamaño del handle
        ui.barra_desplazamiento_vertical.setStyleSheet(f"""
            QScrollBar
            {{
                background: #292a2b;
                width: 16px;
            }}

            QScrollBar::handle
            {{
                background: #404244;
                min-height: {handle_size}px;
                border-radius: 2px;
            }}

            QScrollBar::handle:hover
            {{
                background: #505254;
            }}

            QScrollBar::add-line, QScrollBar::sub-line
            {{
                background: none;
                border: none;
            }}

            QScrollBar::add-page, QScrollBar::sub-page
            {{
                background: #292a2b;
            }}
        """) # Aplica estilos personalizados al scrollbar

# Maneja el evento de redimensionamiento de la ventana
def evento_redimensionamiento(event):
    ajustar_barra_desplazamiento()

    if doc and page_items:
        # Ajustar todas las páginas al nuevo tamaño
        viewport_height = ui.visor_pdf.viewport().height()
        viewport_width = ui.visor_pdf.viewport().width()

        first_page = page_items[0]
        first_page_pixmap = first_page.pixmap()
        page_ratio = first_page_pixmap.width() / first_page_pixmap.height()

        # Calcular nuevo tamaño manteniendo relación de aspecto
        new_height = viewport_height
        new_width = new_height * page_ratio

        # Si es más ancho que el viewport, ajustar al ancho
        if new_width > viewport_width:
            new_width = viewport_width
            new_height = new_width / page_ratio

        # Ajustar la vista
        ui.visor_pdf.fitInView(first_page, PySide6.QtCore.Qt.KeepAspectRatio)

# FUNCIONES DE MANEJO DE ARCHIVOS
# Abre uno o varios archivos PDF mediante un cuadro de diálogo
def abrir_pdf():
    file_paths, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
        vent_princ, "Abrir PDF(s)", "", "PDF Files (*.pdf)") # Abre diálogo para seleccionar archivos PDF

    if file_paths: # Si se seleccionaron archivos
        for file_path in file_paths: # Itera sobre cada archivo seleccionado
            cargar_pdf(file_path) # Carga cada archivo PDF

# Carga un archivo PDF en una nueva pestaña
def cargar_pdf(file_path):
    global doc, current_file # Declara variables globales que se modificarán

    try:
        new_doc = fitz.open(file_path) # Abre el archivo PDF con PyMuPDF
        tab_index = ui.barra_pestanas.addTab(os.path.basename(file_path)) # Añade nuevo tab con nombre del archivo
        docs[tab_index] = new_doc # Almacena el documento en el diccionario

        ui.barra_pestanas.setCurrentIndex(tab_index) # Cambia al tab recién creado
        doc = new_doc # Actualiza el documento actual
        current_file = file_path # Actualiza el archivo actual
        mostrar_paginas_pdf() # Muestra las páginas del PDF
        ajustar_barra_desplazamiento() # Ajusta la barra de desplazamiento
        centrar_primera_pagina() # Centra la primera página

    except Exception as e:
        print(f"Error al cargar PDF: {e}") # Muestra error en consola si falla la carga

# Renderiza y muestra las páginas del PDF en la vista
def mostrar_paginas_pdf():
    global page_items

    if not doc:
        return

    limpiar_vista_pdf()
    y_pos = 0

    # Obtener el tamaño disponible del visor PDF
    viewport_height = ui.visor_pdf.viewport().height()
    viewport_width = ui.visor_pdf.viewport().width()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Calcular la escala necesaria para que la página se ajuste al alto del visor
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height

        # Calcular factor de escala basado en la altura del visor
        scale_factor = (viewport_height - page_spacing) / page_height

        # Asegurarse de que también se ajuste al ancho si es necesario
        if (page_width * scale_factor) > viewport_width:
            scale_factor = viewport_width / page_width

        # Renderizar con la escala calculada
        matrix = fitz.Matrix(scale_factor, scale_factor)
        pix = page.get_pixmap(matrix=matrix)

        image = PySide6.QtGui.QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            PySide6.QtGui.QImage.Format_RGB888)

        pixmap = PySide6.QtGui.QPixmap.fromImage(image)
        item = PySide6.QtWidgets.QGraphicsPixmapItem(pixmap)
        item.setPos(0, y_pos)
        scene.addItem(item)
        page_items.append(item)

        y_pos += pixmap.height() + page_spacing

    if page_items:
        total_height = y_pos - page_spacing
        scene.setSceneRect(PySide6.QtCore.QRectF(0, 0, page_items[0].pixmap().width(), total_height))

    # Ajustar la vista para que la primera página se vea completa
    if page_items:
        ui.visor_pdf.fitInView(page_items[0], PySide6.QtCore.Qt.KeepAspectRatio)

# Exportar texto en PDF a TXT
def exportar_txt():
    if not current_file: # Si no hay archivo actual
        return # Sale de la función

# FUNCIÓN PARA MANEJAR LOS LABELS ARRASTRABLES
# Configura el comportamiento arrastrable de las etiquetas en el panel izquierdo
def configurar_etiquetas_arrastrables():
    drag_data = {
        'dragging': False,
        'current_label': None,
        'offset': 0
    }

    # Maneja el evento de presión del ratón sobre las etiquetas
    def evento_presion_raton(event):
        if event.button() == PySide6.QtCore.Qt.LeftButton:
            pos = event.position().toPoint()
            for label in [ui.etiqueta_1, ui.etiqueta_2]:
                if label.geometry().contains(pos):
                    drag_data['dragging'] = True
                    drag_data['current_label'] = label
                    drag_data['offset'] = pos.y() - label.y()
                    break

    # Maneja el evento de movimiento del ratón para arrastrar etiquetas
    def evento_mover_raton(event):
        if drag_data['dragging'] and drag_data['current_label']:
            label = drag_data['current_label']
            other_label = ui.etiqueta_2 if label == ui.etiqueta_1 else ui.etiqueta_1
            pos = event.position().toPoint()

            # Calcular nueva posición
            new_y = pos.y() - drag_data['offset']

            # Limitar para que no salga del panel
            new_y = max(0, min(new_y, ui.panel_izquierdo.height() - label.height()))

            # Verificar colisión con el otro label
            if label == ui.etiqueta_1:
                new_y = min(new_y, other_label.y() - label.height())
            else:
                new_y = max(new_y, other_label.y() + other_label.height())

            # Aplicar nueva posición
            label.move(0, new_y)

    # Maneja el evento de liberación del ratón al terminar de arrastrar
    def evento_soltar_raton(event):
        if event.button() == PySide6.QtCore.Qt.LeftButton:
            drag_data['dragging'] = False
            drag_data['current_label'] = None

    # Instalar los event filters
    ui.panel_izquierdo.mousePressEvent = evento_presion_raton
    ui.panel_izquierdo.mouseMoveEvent = evento_mover_raton
    ui.panel_izquierdo.mouseReleaseEvent = evento_soltar_raton

# CONEXIONES DE EVENTOS Y SEÑALES
# Conectar acciones del menú
ui.accion_abrir.triggered.connect(abrir_pdf) # Conecta la acción "Abrir" con la función abrir_pdf
ui.accion_exportar.triggered.connect(exportar_txt) # Conecta la acción "Exportar" con la función exportar_txt

# Conectar eventos de tabs
ui.barra_pestanas.tabCloseRequested.connect(cerrar_pestana) # Conecta la señal de cierre de tab
ui.barra_pestanas.currentChanged.connect(cambiar_pestana) # Conecta la señal de cambio de tab

# Conectar eventos de scrollbars
ui.barra_desplazamiento_vertical.valueChanged.connect(desplazar_vista_pdf) # Conecta cambios en scrollbar externo

# Conectar evento de redimensionamiento
original_resize_event = vent_princ.resizeEvent # Guarda el evento original de redimensionamiento
vent_princ.resizeEvent = lambda event: (original_resize_event(event), evento_redimensionamiento(event)) # Combina evento original con handler personalizado

# Configurar los labels arrastrables
configurar_etiquetas_arrastrables()

# PUNTO DE PARTIDA DE LA APLICACIÓN
vent_princ.show() # Muestra la ventana principal
sys.exit(app.exec()) # Inicia el bucle de eventos y termina cuando se cierra la aplicación
