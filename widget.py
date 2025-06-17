import sys # Módulo para funciones del sistema
import os # Módulo para operaciones del sistema operativo
import PySide6.QtWidgets # Módulo para widgets de UI
import PySide6.QtGui # Módulo para componentes gráficos
import PySide6.QtCore # Módulo para funcionalidades básicas de Qt
import fitz # Librería PyMuPDF para manejo de archivos PDF
import ui_form # Módulo con la interfaz de usuario generada
import rango_paginas # Ventana para rango de páginas
import acerca_de # Ventana acerca de

# CONFIGURACIÓN DE LA APLICACIÓN
app_val = PySide6.QtWidgets.QApplication(sys.argv) # Crea la aplicación Qt

if hasattr(sys, 'frozen'): # Si la aplicación está compilada (ejecutable)
    os.environ["PATH"] += os.pathsep + PySide6.QtCore.QLibraryInfo.location(PySide6.QtCore.QLibraryInfo.BinariesPath) # Añade binarios Qt al PATH

# Crear el widget principal
vent_princ = PySide6.QtWidgets.QWidget() # Crea el widget principal de la aplicación

ui_val = ui_form.Ui_Widget() # Crea instancia de la interfaz de usuario
ui_val.setupUi(vent_princ) # Configura la interfaz en el widget principal

# VARIABLES PARA REDIMENSIONAR
altura_inicial_panel_izquierdo = 1
cord_y_etiqueta_1 = 0 # Extremo superior
cord_y_etiqueta_2 = 0

# CONFIGURACIÓN DE LA INTERFAZ DE USUARIO
# Calcular dimensiones de elementos
def renderizar_etiquetas_areas():
    global altura_inicial_panel_izquierdo, cord_y_etiqueta_2

    # Colocar etiquetas arrastrables y áreas de selección a los extremos superior e inferior de la ventana
    ui_val.etiqueta_1.move(0, 0) # Colocar en la parte superior
    ui_val.etiqueta_2.move(0, ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height()) # Colocar en la parte inferior
    ui_val.area_1.move(0, ui_val.etiqueta_1.y()) # Colocar en la parte superior
    ui_val.area_2.move(0, ui_val.etiqueta_2.y()) # Colocar en la parte inferior

    # Expandir áreas de selección horizontalmente
    ui_val.area_1.setGeometry(0, ui_val.etiqueta_1.y(), vent_princ.width() - ui_val.panel_izquierdo.width(), ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), vent_princ.width() - ui_val.panel_izquierdo.width(), ui_val.etiqueta_2.height())

    # Captura de dimensiones
    altura_inicial_panel_izquierdo = ui_val.panel_izquierdo.height() # Altura inicial del panel izquierdo
    cord_y_etiqueta_2 = altura_inicial_panel_izquierdo # Extremo inferior del panel izquierdo

# Realizar dibujado y después calcular dimensiones
PySide6.QtCore.QTimer.singleShot(0, renderizar_etiquetas_areas)

# Configurar escena gráfica para PDF
scene = PySide6.QtWidgets.QGraphicsScene() # Crea nueva escena gráfica

ui_val.visor_pdf.setScene(scene) # Asigna la escena a la vista PDF
ui_val.visor_pdf.setRenderHints(PySide6.QtGui.QPainter.Antialiasing | PySide6.QtGui.QPainter.SmoothPixmapTransform | PySide6.QtGui.QPainter.TextAntialiasing) # Configura renderizado de alta calidad
ui_val.visor_pdf.setAlignment(PySide6.QtCore.Qt.AlignCenter) # Centra el contenido en la vista

# Configurar barras de desplazamiento
ui_val.visor_pdf.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAsNeeded) # Muestra scrollbar vertical cuando sea necesario
ui_val.visor_pdf.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff) # Oculta scrollbar horizontal interno

# Configurar estilos de la barra de pestañas
tab_close_button_style = """
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

ui_val.barra_pestanas.setStyleSheet(ui_val.barra_pestanas.styleSheet() + tab_close_button_style) # Aplica los estilos al tab bar

# VARIABLES GLOBALES
current_file = None # Archivo PDF actualmente abierto
doc = None # Documento PDF actual
docs = {} # Diccionario que almacena todos los documentos abiertos por índice de tab
page_items = [] # Lista de elementos gráficos de páginas PDF

# FUNCIONES DE GESTIÓN DE INTERFAZ
# Maneja el cambio de pestaña en la interfaz
def cambiar_pestana(index):
    global doc, current_file # Declara variables globales que se modificarán

    if index >= 0 and index in docs: # Verifica que el índice sea válido y exista en docs
        doc = docs[index] # Cambia al documento del tab seleccionado
        current_file = doc.name # Actualiza el archivo actual
        mostrar_paginas_pdf() # Muestra las páginas del nuevo documento
        centrar_primera_pagina() # Centra la primera página

# Cierra una pestaña abierta y gestiona los recursos asociados
def cerrar_pestana(index):
    global current_file, doc # Declara variables globales que se modificarán

    if index in docs: # Si el índice existe en docs
        docs[index].close() # Cierra el documento

        del docs[index] # Elimina el documento del diccionario

    ui_val.barra_pestanas.removeTab(index) # Remueve el tab de la barra

    if ui_val.barra_pestanas.count() == 0: # Si no quedan tabs abiertos
        limpiar_vista_pdf() # Limpia la vista PDF
        current_file = None # Reinicia el archivo actual
        doc = None # Reinicia el documento actual

# Centra la primera página del documento en la vista
def centrar_primera_pagina():
    if not page_items: # Si no hay páginas cargadas
        return # Sale de la función

    PySide6.QtCore.QTimer.singleShot(50, lambda: ui_val.visor_pdf.fitInView(page_items[0], PySide6.QtCore.Qt.KeepAspectRatio)) # Centra la primera página después de 50ms manteniendo proporción

# Limpia la vista del PDF y reinicia los elementos relacionados
def limpiar_vista_pdf():
    global page_items # Declara variable global que se modificará

    scene.clear() # Limpia todos los elementos de la escena
    page_items = [] # Reinicia la lista de páginas

# Ajusta el contenido del visor PDF
def ajustar_contenido():
    if not doc or not page_items: # Si no hay documento o páginas
        return # Sale de la función

    view_height = ui_val.visor_pdf.viewport().height() # Obtiene altura del viewport
    content_height = scene.sceneRect().height() # Obtiene altura del contenido

    if page_items:
        total_height = sum(item.pixmap().height() for item in page_items)
        scene.setSceneRect(PySide6.QtCore.QRectF(0, 0, page_items[0].pixmap().width(), total_height))

# Maneja el evento de redimensionamiento de la ventana
def evento_redimensionamiento(event):
    global altura_inicial_panel_izquierdo, cord_y_etiqueta_1, cord_y_etiqueta_2

    # Calcular ratio del panel izquierdo después de redimensionar
    ratio_panel_izquierdo = ui_val.panel_izquierdo.height() / altura_inicial_panel_izquierdo

    # Normalización de posiciones de etiquetas
    norm_cord_y_etiqueta_1 = round(ratio_panel_izquierdo * cord_y_etiqueta_1)
    norm_cord_y_etiqueta_2 = round(ratio_panel_izquierdo * cord_y_etiqueta_2) - ui_val.etiqueta_2.height()

    # Desplazar etiquetas según el ratio del panel izquierdo calculado
    ui_val.etiqueta_1.move(0, max(0, min(norm_cord_y_etiqueta_1, ui_val.etiqueta_2.y() - ui_val.etiqueta_1.height())))
    ui_val.etiqueta_2.move(0, min(ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height(), max(norm_cord_y_etiqueta_2, ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())))

    # Mover áreas selección a la par con las etiquetas
    ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.etiqueta_2.y())








    if doc and page_items:
        # Ajustar todas las páginas al nuevo tamaño
        viewport_height = ui_val.visor_pdf.viewport().height()
        viewport_width = ui_val.visor_pdf.viewport().width()

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
        ui_val.visor_pdf.fitInView(first_page, PySide6.QtCore.Qt.KeepAspectRatio)

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
        tab_index = ui_val.barra_pestanas.addTab(os.path.basename(file_path)) # Añade nuevo tab con nombre del archivo
        docs[tab_index] = new_doc # Almacena el documento en el diccionario

        ui_val.barra_pestanas.setCurrentIndex(tab_index) # Cambia al tab recién creado
        doc = new_doc # Actualiza el documento actual
        current_file = file_path # Actualiza el archivo actual
        mostrar_paginas_pdf() # Muestra las páginas del PDF
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
    viewport_height = ui_val.visor_pdf.viewport().height()
    viewport_width = ui_val.visor_pdf.viewport().width()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Calcular la escala necesaria para que la página se ajuste al alto del visor
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height

        # Calcular factor de escala basado en la altura del visor
        scale_factor = viewport_height / page_height

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

        y_pos += pixmap.height()

    if page_items:
        total_height = y_pos
        scene.setSceneRect(PySide6.QtCore.QRectF(0, 0, page_items[0].pixmap().width(), total_height))

    # Ajustar la vista para que la primera página se vea completa
    if page_items:
        ui_val.visor_pdf.fitInView(page_items[0], PySide6.QtCore.Qt.KeepAspectRatio)

# Exportar texto en PDF a TXT
def exportar_txt():
    if not current_file: # Si no hay archivo actual
        return # Sale de la función
    else:
        #

        return

# FUNCIÓN PARA MANEJAR LOS LABELS ARRASTRABLES
# Configura el comportamiento arrastrable de las etiquetas en el panel izquierdo
def configurar_etiquetas_arrastrables():
    datos_arrastre = { # Diccionario para estado del arrastre
        'arrastrando': False, # Bandera de arrastre activo
        'etiqueta_actual': None, # Referencia a etiqueta actual
        'desfase_val': 0, # Desfase vertical del cursor
        'posicion_inicial_y': 0 # Posición Y inicial de etiqueta
    }

     # Maneja el evento de presión del ratón sobre las etiquetas (actualizar el diccionario según la etiqueta que se presione)
    def evento_presion_raton(evento):
        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Solo botón izquierdo
            posicion = evento.position().toPoint() # Posición del click

            #
            for etiqueta in [ui_val.etiqueta_1, ui_val.etiqueta_2]:
                if etiqueta.geometry().contains(posicion): # Si click está en etiqueta
                    datos_arrastre['arrastrando'] = True # Activar arrastre
                    datos_arrastre['etiqueta_actual'] = etiqueta # Guardar referencia
                    datos_arrastre['desfase_val'] = posicion.y() - etiqueta.y() # Calcular desfase
                    datos_arrastre['posicion_inicial_y'] = etiqueta.y() # Guardar posición inicial

                    break

    # Maneja el evento de movimiento del ratón para arrastrar etiquetas
    def evento_mover_raton(evento):
        global cord_y_etiqueta_1, cord_y_etiqueta_2

        if datos_arrastre['arrastrando'] and datos_arrastre['etiqueta_actual']:
            etiqueta = datos_arrastre['etiqueta_actual'] # Etiqueta siendo arrastrada
            posicion = evento.position().toPoint() # Posición actual del mouse
            tmp_y = posicion.y() - datos_arrastre['desfase_val'] # Nueva posición Y (actualización constante)

            if etiqueta == ui_val.etiqueta_1: # Para etiqueta superior
                tmp_y = max(0, min(tmp_y, ui_val.etiqueta_2.y() - etiqueta.height())) # Límites
                ui_val.area_1.setGeometry(0, 0, ui_val.area_1.width(), tmp_y + etiqueta.height()) #
                cord_y_etiqueta_1 = tmp_y # Actualizar coordenada para etiqueta
            else: # Para etiqueta inferior
                tmp_y = max(ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height(), min(tmp_y, ui_val.panel_izquierdo.height() - etiqueta.height())) # Límites
                ui_val.area_2.setGeometry(0, tmp_y, ui_val.area_2.width(), vent_princ.height() - tmp_y - ui_val.barra_menu.height() - ui_val.barra_pestanas.height()) #
                cord_y_etiqueta_2 = tmp_y + ui_val.etiqueta_2.height() # Actualizar coordenada para etiqueta

            etiqueta.move(0, tmp_y) # Mover etiqueta a nueva posición

    # Maneja el evento de liberación del ratón al terminar de arrastrar
    def evento_soltar_raton(evento):
        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Al soltar botón izquierdo
            datos_arrastre['arrastrando'] = False # Desactivar arrastre
            datos_arrastre['etiqueta_actual'] = None # Limpiar referencia

    # Asignar eventos personalizados al panel
    ui_val.panel_izquierdo.mousePressEvent = evento_presion_raton # Asigna función para presionar ratón
    ui_val.panel_izquierdo.mouseMoveEvent = evento_mover_raton # Asigna función para mover ratón
    ui_val.panel_izquierdo.mouseReleaseEvent = evento_soltar_raton # Asigna función para soltar ratón

# Aplicar márgen a todas las pestañas
def aplicar_margen_pestanas():
    return

# VENTANAS
def mostrar_rango_paginas():
    ventana = rango_paginas.rango_paginas_ui()

    ventana.ventana_ui()
    ventana.exec()

    # Aplicar rango de páginas a la pestaña


# Ventana "Acerca de"
def mostrar_acerca_de():
    ventana = acerca_de.acerca_de_ui()

    ventana.ventana_ui()
    ventana.exec()

# CONEXIONES DE EVENTOS Y SEÑALES
# Conectar acciones del menú
ui_val.accion_abrir.triggered.connect(abrir_pdf) # Conecta la acción "Open" con la función "abrir_pdf"
ui_val.accion_exportar.triggered.connect(exportar_txt) # Conecta la acción "Export" con la "función exportar_txt"
ui_val.accion_aplicar_margen_todas_pestanas.triggered.connect(aplicar_margen_pestanas) # Conecta la acción "Apply Margin to All Tabs" con la función "aplicar_margen_pestanas"
ui_val.accion_rango_paginas.triggered.connect(mostrar_rango_paginas) # Conecta la acción "Pages Range" con la función "mostrar_rango_paginas"
ui_val.accion_acerca_de.triggered.connect(mostrar_acerca_de) # Conecta la acción "About Exakova TextFlow" con la función "mostrar_acerca_de"

# Conectar eventos de pestañas
ui_val.barra_pestanas.tabCloseRequested.connect(cerrar_pestana) # Conecta la señal de cierre de tab
ui_val.barra_pestanas.currentChanged.connect(cambiar_pestana) # Conecta la señal de cambio de tab

# Conectar evento de redimensionamiento
original_resize_event = vent_princ.resizeEvent # Guarda el evento original de redimensionamiento
vent_princ.resizeEvent = lambda event: (original_resize_event(event), evento_redimensionamiento(event)) # Combina evento original con handler personalizado

# Configurar los labels arrastrables
configurar_etiquetas_arrastrables()

# PUNTO DE PARTIDA DE LA APLICACIÓN
vent_princ.show() # Muestra la ventana principal
sys.exit(app_val.exec()) # Inicia el bucle de eventos y termina cuando se cierra la aplicación
