import sys # Módulo para funciones del sistema
import os # Módulo para operaciones del sistema operativo
import PySide6.QtWidgets # Módulo para widgets de UI
import PySide6.QtGui # Módulo para componentes gráficos
import PySide6.QtCore # Módulo para funcionalidades básicas de Qt
import ui_form # Módulo con la interfaz de usuario generada
import fitz # Librería PyMuPDF para manejo de archivos PDF

# Variables globales para el estado de la aplicación
current_file = None # Archivo PDF actualmente abierto
doc = None # Documento PDF actual
docs = {} # Diccionario que almacena todos los documentos abiertos por índice de tab
page_items = [] # Lista de elementos gráficos de páginas PDF
page_spacing = 10 # Espaciado entre páginas en píxeles
scene = None # Escena gráfica para mostrar las páginas PDF
ui = None # Interfaz de usuario principal
main_widget = None # Widget principal de la aplicación

# Configuración de la interfaz de usuario
def setup_ui():
    ui.actionOpen.triggered.connect(open_pdf) # Conecta la acción "Abrir" con la función open_pdf
    ui.actionExport.triggered.connect(export_pdf) # Conecta la acción "Exportar" con la función export_pdf
    ui.actionApply_Margin_to_All_Tabs.triggered.connect(toggle_margin_action) # Conecta la acción de márgenes

def toggle_margin_action():
    current_text = ui.actionApply_Margin_to_All_Tabs.text() # Obtiene el texto actual de la acción
    if "✔" in current_text: # Si ya tiene la marca de verificación
        ui.actionApply_Margin_to_All_Tabs.setText("Apply Margin to All Tabs") # Quita la marca
    else:
        ui.actionApply_Margin_to_All_Tabs.setText("Apply Margin to All Tabs") # Mantiene el texto

def setup_tab_bar():
    ui.tabBar.tabCloseRequested.connect(close_tab) # Conecta la señal de cierre de tab
    ui.tabBar.currentChanged.connect(tab_changed) # Conecta la señal de cambio de tab

    style = """
        QTabBar::close-button
        {
            subcontrol-origin: padding;
            subcontrol-position: right;
            width: 16px;
            height: 16px;
            margin-right: 2px;
        }

        QTabBar::close-button:hover
        {
            background: #505254;
            border-radius: 2px;
        }
    """ # Estilos CSS para el botón de cierre de tabs

    ui.tabBar.setStyleSheet(ui.tabBar.styleSheet() + style) # Aplica los estilos al tab bar

def tab_changed(index):
    global doc, current_file # Declara variables globales que se modificarán
    if index >= 0 and index in docs: # Verifica que el índice sea válido y exista en docs
        doc = docs[index] # Cambia al documento del tab seleccionado
        current_file = doc.name # Actualiza el archivo actual
        display_pdf_pages() # Muestra las páginas del nuevo documento
        adjust_scrollbar() # Ajusta la barra de desplazamiento
        center_first_page() # Centra la primera página

def center_first_page():
    if not page_items: # Si no hay páginas cargadas
        return # Sale de la función

    PySide6.QtCore.QTimer.singleShot(50, lambda: ui.pdfView.fitInView(
        page_items[0],
        PySide6.QtCore.Qt.KeepAspectRatio
    )) # Centra la primera página después de 50ms manteniendo proporción

def close_tab(index):
    global current_file, doc # Declara variables globales que se modificarán
    if index in docs: # Si el índice existe en docs
        docs[index].close() # Cierra el documento
        del docs[index] # Elimina el documento del diccionario

    ui.tabBar.removeTab(index) # Remueve el tab de la barra

    if ui.tabBar.count() == 0: # Si no quedan tabs abiertos
        clear_pdf_view() # Limpia la vista PDF
        current_file = None # Reinicia el archivo actual
        doc = None # Reinicia el documento actual

def setup_scrollbars():
    ui.verticalScrollBar.valueChanged.connect(scroll_pdf_view) # Conecta cambios en scrollbar externo
    ui.pdfView.verticalScrollBar().valueChanged.connect(
        lambda v: ui.verticalScrollBar.setValue(v)) # Sincroniza scrollbar interno con externo
    ui.pdfView.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Oculta scrollbar vertical interno
    ui.pdfView.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Oculta scrollbar horizontal interno

def scroll_pdf_view(value):
    ui.pdfView.verticalScrollBar().setValue(value) # Sincroniza el desplazamiento de la vista PDF

def setup_pdf_view():
    global scene # Declara variable global que se modificará
    scene = PySide6.QtWidgets.QGraphicsScene() # Crea nueva escena gráfica
    ui.pdfView.setScene(scene) # Asigna la escena a la vista PDF
    ui.pdfView.setRenderHints(
        PySide6.QtGui.QPainter.Antialiasing |
        PySide6.QtGui.QPainter.SmoothPixmapTransform |
        PySide6.QtGui.QPainter.TextAntialiasing) # Configura renderizado de alta calidad
    ui.pdfView.setAlignment(PySide6.QtCore.Qt.AlignCenter) # Centra el contenido en la vista

def clear_pdf_view():
    global page_items # Declara variable global que se modificará
    scene.clear() # Limpia todos los elementos de la escena
    page_items = [] # Reinicia la lista de páginas
    ui.verticalScrollBar.setVisible(False) # Oculta la barra de desplazamiento

def open_pdf():
    file_paths, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
        main_widget, "Abrir PDF(s)", "", "PDF Files (*.pdf)") # Abre diálogo para seleccionar archivos PDF

    if file_paths: # Si se seleccionaron archivos
        for file_path in file_paths: # Itera sobre cada archivo seleccionado
            load_pdf(file_path) # Carga cada archivo PDF

def load_pdf(file_path):
    global doc, current_file # Declara variables globales que se modificarán
    try:
        new_doc = fitz.open(file_path) # Abre el archivo PDF con PyMuPDF
        tab_index = ui.tabBar.addTab(os.path.basename(file_path)) # Añade nuevo tab con nombre del archivo
        docs[tab_index] = new_doc # Almacena el documento en el diccionario

        # Configurar botón de cierre
        close_button = PySide6.QtWidgets.QPushButton("❌") # Crea botón de cierre con emoji
        close_button.setStyleSheet("""
            QPushButton
            {
                color: white;
                border: none;
                padding: 0px;
                font-size: 10px;
            }

            QPushButton:hover
            {
                background: #505254;
                border-radius: 2px;
            }
        """) # Estilos CSS para el botón de cierre
        close_button.setFixedSize(16, 16) # Establece tamaño fijo del botón
        close_button.clicked.connect(lambda: close_tab(tab_index)) # Conecta click con cierre de tab
        ui.tabBar.setTabButton(tab_index, PySide6.QtWidgets.QTabBar.RightSide, close_button) # Añade botón al tab

        ui.tabBar.setCurrentIndex(tab_index) # Cambia al tab recién creado
        doc = new_doc # Actualiza el documento actual
        current_file = file_path # Actualiza el archivo actual
        display_pdf_pages() # Muestra las páginas del PDF
        adjust_scrollbar() # Ajusta la barra de desplazamiento
        center_first_page() # Centra la primera página

    except Exception as e:
        print(f"Error al cargar PDF: {e}") # Muestra error en consola si falla la carga

def display_pdf_pages():
    global page_items # Declara variable global que se modificará
    if not doc: # Si no hay documento cargado
        return # Sale de la función

    clear_pdf_view() # Limpia la vista actual
    y_pos = 0 # Posición vertical inicial

    for page_num in range(len(doc)): # Itera sobre cada página del documento
        page = doc.load_page(page_num) # Carga la página actual
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Renderiza página con escala 2x para mejor calidad
        image = PySide6.QtGui.QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            PySide6.QtGui.QImage.Format_RGB888) # Convierte a QImage

        pixmap = PySide6.QtGui.QPixmap.fromImage(image) # Convierte QImage a QPixmap
        item = PySide6.QtWidgets.QGraphicsPixmapItem(pixmap) # Crea item gráfico con la imagen
        item.setPos(0, y_pos) # Posiciona el item en la escena
        scene.addItem(item) # Añade el item a la escena
        page_items.append(item) # Añade el item a la lista de páginas

        y_pos += pixmap.height() + page_spacing # Calcula posición para la siguiente página

    if page_items: # Si hay páginas cargadas
        total_height = y_pos - page_spacing # Calcula altura total del contenido
        scene.setSceneRect(PySide6.QtCore.QRectF(0, 0, page_items[0].pixmap().width(), total_height)) # Establece área de la escena

def adjust_scrollbar():
    if not doc or not page_items: # Si no hay documento o páginas
        ui.verticalScrollBar.setVisible(False) # Oculta la barra de desplazamiento
        return # Sale de la función

    view_height = ui.pdfView.viewport().height() # Obtiene altura del viewport
    content_height = scene.sceneRect().height() # Obtiene altura del contenido
    needs_scrollbar = content_height > view_height # Determina si necesita scrollbar

    ui.verticalScrollBar.setVisible(needs_scrollbar) # Muestra/oculta scrollbar según necesidad

    if needs_scrollbar: # Si necesita scrollbar
        pdf_scrollbar = ui.pdfView.verticalScrollBar() # Obtiene scrollbar interno
        ui.verticalScrollBar.setRange(0, pdf_scrollbar.maximum()) # Establece rango del scrollbar externo
        ui.verticalScrollBar.setPageStep(pdf_scrollbar.pageStep()) # Sincroniza paso de página
        ui.verticalScrollBar.setSingleStep(pdf_scrollbar.singleStep()) # Sincroniza paso simple

        visible_ratio = view_height / content_height # Calcula proporción visible
        handle_size = max(20, int(ui.verticalScrollBar.height() * visible_ratio)) # Calcula tamaño del handle
        ui.verticalScrollBar.setStyleSheet(f"""
            QScrollBar {{
                background: #292a2b;
                width: 16px;
            }}
            QScrollBar::handle {{
                background: #404244;
                min-height: {handle_size}px;
                border-radius: 2px;
            }}
            QScrollBar::handle:hover {{
                background: #505254;
            }}
            QScrollBar::add-line, QScrollBar::sub-line {{
                background: none;
                border: none;
            }}
            QScrollBar::add-page, QScrollBar::sub-page {{
                background: #292a2b;
            }}
        """) # Aplica estilos personalizados al scrollbar

def export_pdf():
    if not current_file: # Si no hay archivo actual
        return # Sale de la función
    print(f"Exportando {current_file}...") # Mensaje de debug para exportación

def handle_resize_event(event):
    adjust_scrollbar() # Ajusta scrollbar cuando cambia el tamaño
    if doc and page_items: # Si hay documento y páginas cargadas
        view_width = ui.pdfView.viewport().width() # Obtiene ancho del viewport
        for item in page_items: # Itera sobre cada página
            if item.pixmap().width() > view_width: # Si la página es más ancha que la vista
                ui.pdfView.fitInView(item, PySide6.QtCore.Qt.KeepAspectRatio) # Ajusta la vista manteniendo proporción
                break # Sale del bucle después del primer ajuste

# Punto de partida de la aplicación
app = PySide6.QtWidgets.QApplication(sys.argv) # Crea la aplicación Qt

if hasattr(sys, 'frozen'): # Si la aplicación está compilada (ejecutable)
    os.environ["PATH"] += os.pathsep + PySide6.QtCore.QLibraryInfo.location(PySide6.QtCore.QLibraryInfo.BinariesPath) # Añade binarios Qt al PATH

# Crear el widget principal
main_widget = PySide6.QtWidgets.QWidget() # Crea el widget principal de la aplicación
ui = ui_form.Ui_Widget() # Crea instancia de la interfaz de usuario
ui.setupUi(main_widget) # Configura la interfaz en el widget principal

# Configuración inicial de todos los componentes
setup_ui() # Configura acciones y conexiones de la interfaz
setup_scrollbars() # Configura las barras de desplazamiento
setup_pdf_view() # Configura la vista para mostrar PDFs
setup_tab_bar() # Configura la barra de tabs

# Conectar el evento de redimensionamiento
original_resize_event = main_widget.resizeEvent # Guarda el evento original de redimensionamiento
main_widget.resizeEvent = lambda event: (original_resize_event(event), handle_resize_event(event)) # Combina evento original con handler personalizado

main_widget.show() # Muestra la ventana principal
sys.exit(app.exec()) # Inicia el bucle de eventos y termina cuando se cierra la aplicación
