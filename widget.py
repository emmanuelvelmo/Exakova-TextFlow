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
ui_val.iniciar_ui(vent_princ) # Configura la interfaz en el widget principal

# VARIABLES
# Variables para redimensionar
altura_panel_izquierdo = 1
cord_y_etiqueta_1 = 0 # Extremo superior
cord_y_etiqueta_2 = 0

# Variables de rango de páginas
pags_inicio = {}
pags_fin = {}

# Variables de margenes
margen_bool = True
margenes_superiores = []
margenes_inferiores = []

# Variables para el control de la barra de desplazamiento vertical
pag_actual = {}
num_pags = {}
frac_pag = {}

# Variables para manejo de archivos
archivo_iter = None # Archivo PDF actualmente abierto
doc = None # Documento PDF actual
docs_dicc = {} # Diccionario que almacena todos los documentos abiertos por índice de tab
pagina_arts = [] # Lista de elementos gráficos de páginas PDF
pags_actual = [] # Página actual de cada pestaña (se actualiza al cambiar de página)

# CONFIGURACIÓN DE LA INTERFAZ DE USUARIO
# Calcular dimensiones de elementos
def renderizar_etiquetas_areas():
    global altura_panel_izquierdo, cord_y_etiqueta_2

    # Colocar etiquetas arrastrables a los extremos superior e inferior de la ventana
    ui_val.etiqueta_1.move(0, 0) # Colocar en la parte superior
    ui_val.etiqueta_2.move(0, ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height()) # Colocar en la parte inferior

    # Expandir áreas de selección horizontalmente
    ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

    # Captura de dimensiones
    altura_panel_izquierdo = ui_val.panel_izquierdo.height() # Altura inicial del panel izquierdo
    cord_y_etiqueta_2 = altura_panel_izquierdo # Extremo inferior del panel izquierdo

# Realizar dibujado y después calcular dimensiones
PySide6.QtCore.QTimer.singleShot(0, renderizar_etiquetas_areas)

# Configurar escena gráfica para PDF
escena = PySide6.QtWidgets.QGraphicsScene() # Crea nueva escena gráfica

ui_val.visor_pdf.setScene(escena) # Asigna la escena a la vista PDF
ui_val.visor_pdf.setRenderHints(PySide6.QtGui.QPainter.Antialiasing | PySide6.QtGui.QPainter.SmoothPixmapTransform | PySide6.QtGui.QPainter.TextAntialiasing) # Configura renderizado de alta calidad

# FUNCIONES DE MANEJO DE ARCHIVOS
# Carga un archivo PDF en una nueva pestaña
def cargar_pdf(archivo_dir):
    global doc, docs_dicc, archivo_iter # Declara variables globales que se modificarán

    try:
        nuevo_doc = fitz.open(archivo_dir) # Abre el archivo PDF con PyMuPDF en memoria

        tab_indice = ui_val.barra_pestanas.addTab(os.path.basename(archivo_dir)) # Añade nueva pestaña con nombre del archivo
        docs_dicc[tab_indice] = nuevo_doc # Almacena el documento en el diccionario
        ui_val.barra_pestanas.setCurrentIndex(tab_indice) # Cambia al tab recién creado

        doc = nuevo_doc # Actualiza el documento actual
        archivo_iter = archivo_dir # Actualiza el archivo actual

        # Agregar rango de páginas del documento al diccionario
        pags_inicio[tab_indice] = 1
        pags_fin[tab_indice] = len(doc) # Asignar el número total de páginas del documento

        ventana_paginas_pdf(tab_indice) # Muestra las páginas del PDF
    except Exception as e:
        pass #

# FUNCIONES DE INTERFAZ
# Maneja el evento de redimensionamiento de la ventana
def evento_redimensionamiento(evento):
    global altura_panel_izquierdo, cord_y_etiqueta_1, cord_y_etiqueta_2, num_pags, frac_pag

    # Calcular ratio del panel izquierdo después de redimensionar
    ratio_panel_izquierdo = ui_val.panel_izquierdo.height() / altura_panel_izquierdo

    # Normalización de posiciones de etiquetas
    norm_cord_y_etiqueta_1 = round(ratio_panel_izquierdo * cord_y_etiqueta_1)
    norm_cord_y_etiqueta_2 = round(ratio_panel_izquierdo * cord_y_etiqueta_2) - ui_val.etiqueta_2.height()

    # Desplazar etiquetas según el ratio del panel izquierdo calculado
    ui_val.etiqueta_1.move(0, max(0, min(norm_cord_y_etiqueta_1, ui_val.etiqueta_2.y() - ui_val.etiqueta_1.height())))
    ui_val.etiqueta_2.move(0, min(ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height(), max(norm_cord_y_etiqueta_2, ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())))

    # Mover áreas selección a la par con las etiquetas
    ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

    if doc and pagina_arts:
        # Ajustar todas las páginas al nuevo tamaño
        viewport_height = ui_val.visor_pdf.viewport().height()
        viewport_width = ui_val.visor_pdf.viewport().width()

        first_page = pagina_arts[0]
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

    # Ajustar barra scroll si está habilitada
    #if ui_val.barra_desp_vert.isVisible():
        # Ajustar fracción por página
        #frac_pag = round(ui_val.visor_pdf.height() / num_pags[])

        # Asignar a barra en scroll la fracción de la altura de una sóla página y estilo
        #ui_val.barra_desp_vert.setStyleSheet(f"""
        """
            QScrollBar:vertical
            {{
                width: 16px;
            }}

            QScrollBar::handle:vertical
            {{
                background: #404244;
                min-height: {frac_pag}px; /* Altura dinámica */
            }}

            QScrollBar::handle:vertical:hover
            {{
                background: #505254;
            }}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {{
                background: #292a2b;
            }}
        """#)

# Limpia la vista del PDF y reinicia los elementos relacionados
def limpiar_vista_pdf():
    global pagina_arts # Declara variable global que se modificará

    escena.clear() # Limpia todos los elementos de la escena
    pagina_arts = [] # Reinicia la lista de páginas

# Maneja el cambio de pestaña en la interfaz
def cambiar_pestana(indice_val):
    global doc, archivo_iter # Declara variables globales que se modificarán

    if indice_val >= 0 and indice_val in docs_dicc: # Verifica que el índice sea válido y exista en docs_dicc
        doc = docs_dicc[indice_val] # Cambia al documento del tab seleccionado
        archivo_iter = doc.name # Actualiza el archivo actual

        ventana_paginas_pdf(indice_val) # Muestra las páginas del nuevo documento

# Cierra una pestaña abierta y gestiona los recursos asociados
def cerrar_pestana(indice_val):
    global archivo_iter, doc # Declara variables globales que se modificarán

    if indice_val in docs_dicc: # Si el índice existe en docs_dicc
        docs_dicc[indice_val].close() # Cierra el documento

        del docs_dicc[indice_val] # Elimina el documento del diccionario

    ui_val.barra_pestanas.removeTab(indice_val) # Remueve el tab de la barra

    if ui_val.barra_pestanas.count() == 0: # Si no quedan tabs abiertos
        limpiar_vista_pdf() # Limpia la vista PDF

        ui_val.barra_desp_vert.setVisible(False) # Ocultar la barra scroll

        archivo_iter = None # Reinicia el archivo actual
        doc = None # Reinicia el documento actual

# Renderiza y muestra las páginas del PDF en la vista
def ventana_paginas_pdf(indice_val):
    global pagina_arts, num_pags, pag_actual

    pag_actual[indice_val] = 1 # Actualizar a primera página en diccionario

    if not doc:
        pass
    else:
        y_pos = 0
        pagina_arts = [] # Reiniciar la lista de páginas # CONSIDERAR ELIMINAR

        # Obtener el número de páginas y almacenarlo en el diccionario
        num_pags[indice_val] = len(doc)

        viewport_height = ui_val.visor_pdf.viewport().height()
        viewport_width = ui_val.visor_pdf.viewport().width()

        for page_num in range(num_pags[indice_val]): # Usar el valor del diccionario
            page = doc.load_page(page_num)
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height

            scale_factor = viewport_height / page_height
            if (page_width * scale_factor) > viewport_width:
                scale_factor = viewport_width / page_width

            matrix = fitz.Matrix(scale_factor, scale_factor)
            pix = page.get_pixmap(matrix=matrix)
            image = PySide6.QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, PySide6.QtGui.QImage.Format_RGB888)
            pixmap = PySide6.QtGui.QPixmap.fromImage(image)
            item = PySide6.QtWidgets.QGraphicsPixmapItem(pixmap)
            item.setPos(0, y_pos)
            escena.addItem(item)
            pagina_arts.append(item)
            y_pos += pixmap.height()

        if pagina_arts:
            total_height = y_pos
            escena.setSceneRect(PySide6.QtCore.QRectF(0, 0, pagina_arts[0].pixmap().width(), total_height))
            ui_val.visor_pdf.fitInView(pagina_arts[0], PySide6.QtCore.Qt.KeepAspectRatio)

        ui_val.visor_pdf.wheelEvent = voluta_desp

        # Verificar si hay más de una página usando el diccionario
        if num_pags[indice_val] > 1:
            configurar_barra_desp(indice_val) #

# CONFIGURACIONES PERSONALIZADAS
#############################################################################################################
# Comportamiento de voluta del mouse
def voluta_desp(evento):
    # Obtener la barra de desplazamiento vertical
    scroll_bar = ui_val.visor_pdf.verticalScrollBar()

    # Determinar la dirección del scroll (positivo = abajo, negativo = arriba)
    delta = evento.angleDelta().y()

    if delta > 0: # Scroll hacia arriba
        scroll_bar.setValue(scroll_bar.value() - scroll_bar.pageStep()) # Ir a la página anterior
        # Actualizar posición de la barra scroll
    else: # Scroll hacia abajo
        scroll_bar.setValue(scroll_bar.value() + scroll_bar.pageStep()) # Ir a la página siguiente
        # Actualizar posición de la barra scroll

    evento.accept() #

# Comportamiento de etiquetas en panel izquierdo
def configurar_etiquetas_arrastrables():
    datos_arrastre = { # Diccionario para estado del arrastre
        'arrastrando': False, # Bandera de arrastre activo
        'etiqueta_actual': None, # Referencia a etiqueta actual
        'desfase_val': 0, # Desfase vertical del cursor
        'posicion_inicial_y': 0 # Posición Y inicial de etiqueta
    }

     # Maneja el evento de presión del ratón sobre las etiquetas (actualizar el diccionario según la etiqueta que se presione)
    def evento_presion_raton(evento):
        global altura_panel_izquierdo

        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Solo botón izquierdo
            altura_panel_izquierdo = ui_val.panel_izquierdo.height() # Actualizar altura de panel izquierdo

            posicion = evento.position().toPoint() # Posición del click

            #
            for etiqueta in [ui_val.etiqueta_1, ui_val.etiqueta_2]:
                if etiqueta.geometry().contains(posicion): # Si click está en etiqueta
                    datos_arrastre['arrastrando'] = True # Activar arrastre
                    datos_arrastre['etiqueta_actual'] = etiqueta # Guardar referencia
                    datos_arrastre['desfase_val'] = posicion.y() - etiqueta.y() # Calcular desfase
                    datos_arrastre['posicion_inicial_y'] = etiqueta.y() # Guardar posición inicial

                    break

            evento.accept() #

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
                cord_y_etiqueta_2 = ui_val.etiqueta_2.y() + ui_val.etiqueta_2.height() # Actualiar posición de la etique sin mover
            else: # Para etiqueta inferior
                tmp_y = max(ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height(), min(tmp_y, ui_val.panel_izquierdo.height() - etiqueta.height())) # Límites
                ui_val.area_2.setGeometry(0, tmp_y, ui_val.area_2.width(), vent_princ.height() - tmp_y - ui_val.barra_menu.height() - ui_val.barra_pestanas.height()) #
                cord_y_etiqueta_2 = tmp_y + ui_val.etiqueta_2.height() # Actualizar coordenada para etiqueta
                cord_y_etiqueta_1 = ui_val.etiqueta_1.y() # Actualiar posición de la etique sin mover

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

# Comportamiento de scroll
def configurar_barra_desp(indice_val):
    global altura_barra_desp, num_pags, frac_pag

    # Variables
    scrollbar_pressed = False
    scrollbar_press_pos = 0
    scrollbar_press_value = 0

    # Alto en píxeles de una página respecto a la altura de scrollbar
    frac_pag = round(ui_val.visor_pdf.height() / num_pags[indice_val])

    # Asignar a barra en scroll la fracción de la altura de una sóla página y estilo
    ui_val.barra_desp_vert.setStyleSheet(f"""
        QScrollBar:vertical
        {{
            width: 16px;
        }}

        QScrollBar::handle:vertical
        {{
            background: #404244;
            min-height: {frac_pag}px; /* Altura dinámica */
        }}

        QScrollBar::handle:vertical:hover
        {{
            background: #505254;
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {{
            background: #292a2b;
        }}
    """)

    # Mostrar la barra scroll
    ui_val.barra_desp_vert.setVisible(True)

    # Al presionar sobre el scroll
    def scrollbar_press_event(evento):
        global frac_pag, pag_actual, pagina_arts

        if evento.button() == PySide6.QtCore.Qt.LeftButton: #
            scrollbar_pressed = True #

            # Obtener posición del cursor
            pos_cursor = evento.position().toPoint()

            # Obtener número de página en base a altura del cursor
            pos_pag = int(pos_cursor.y() / frac_pag)

            # Cambiar página si aplica
            if pag_actual[indice_val] != pos_pag:
                # Cambiar a nueva página
                ui_val.visor_pdf.centerOn(pagina_arts[pos_pag])

                # Actualizar página actual
                pag_actual[indice_val] = pos_pag

                # Mover handler a posición
                ui_val.barra_desp_vert.setValue(pos_pag * frac_pag)

            evento.accept() #

    # Al mover la barra de scroll
    def scrollbar_move_event(evento):
        global num_pags, frac_pag, pag_actual

        # Se presiona el handler
        if scrollbar_pressed:
            # Obtener posición del cursor
            pos_cursor = evento.position().toPoint()

            # Mover la barra con el cursor
            ui_val.barra_desp_vert.setValue(pos_cursor.y())

            # Obtener número de página en base a altura del cursor
            pos_pag = int(pos_cursor.y() / frac_pag)

            # Cambiar página si aplica
            if pag_actual[indice_val] != pos_pag:
                # Cambiar a nueva página
                ui_val.visor_pdf.centerOn(pagina_arts[pos_pag])

                # Actualizar página actual
                pag_actual[indice_val] = pos_pag

            evento.accept() #

    # Soltar el botón izquierdo del mouse
    def scrollbar_release_event(evento):
        global scrollbar_pressed

        if evento.button() == PySide6.QtCore.Qt.LeftButton:
            scrollbar_pressed = False

            evento.accept() #

    # Asignar los eventos personalizados al scrollbar
    ui_val.barra_desp_vert.mousePressEvent = scrollbar_press_event
    ui_val.barra_desp_vert.mouseMoveEvent = scrollbar_move_event
    ui_val.barra_desp_vert.mouseReleaseEvent = scrollbar_release_event

# FUNCIONES DE ACCIONES
# Abre uno o varios archivos PDF mediante un cuadro de diálogo
def abrir_pdf():
    archivos_ruta, filtro_val = PySide6.QtWidgets.QFileDialog.getOpenFileNames(vent_princ, "Open PDF(s)", "", "PDF Files (*.pdf)") # Abre diálogo para seleccionar archivos PDF

    if archivos_ruta: # Si se seleccionaron archivos
        # Itera sobre cada archivo seleccionado
        for archivo_dir in archivos_ruta: # Itera sobre cada ruta seleccionada
            cargar_pdf(archivo_dir) # Carga cada archivo PDF

# Exportar texto en PDF a TXT
def exportar_txt():
    global margen_bool, margenes_superiores, margenes_inferiores, docs_dicc

    if not docs_dicc: # Si no hay archivos
        return # Salir de la función
    else:
        # Variables

        texto_docs = [] #
        texto_pag = "" #



        # Aplica el mismo margen para todos los archivos
        if margen_bool:
            # Iterar sobre cada archivo
            for iter_doc in docs_dicc:
                # Obtener altura de la primera página
                altura_pagina = pagina_arts[0].pixmap().height()

                # Convertir la altura de los márgenes a fracción del total de la página (el mismo para todos los documentos)
#########################################################################################################################
                margenes_superiores[0] = round(cord_y_etiqueta_1 / altura_pagina) # CORREGIR
                margenes_inferiores[0] = round(cord_y_etiqueta_1 / altura_pagina) # CORREGIR

                # Generar área de texto elegible en la página
                area_texto = "" #

                # Iterar sobre el rango de páginas del archivo
                for pags_inicio[iter_doc] in pags_final[iter_doc]:
                    # Extraer texto del área (acumular progreseivamente página por página en variable)
                    texto_pag = page.get_text("text", clip = area_texto) #
                    texto_docs[iter_doc] += texto_pag
        # Aplicar márgenes distintos a cada archivos
        else:
            # Iterar sobre cada archivo
            for iter_doc in docs_dicc:
                # Obtener altura de la primera página
                altura_pagina = pagina_arts[0].pixmap().height()

                # Convertir la altura de los márgenes a fracción del total de la página (distinto para cada documento)
                margenes_superiores[0] = round(cord_y_etiqueta_1 / altura_pagina) # CORREGIR
                margenes_inferiores[0] = round(cord_y_etiqueta_1 / altura_pagina) # CORREGIR

                # Generar área de texto elegible en la página
                area_texto = "" #

                # Iterar sobre el rango de páginas del archivo
                for pags_inicio[iter_doc] in pags_final[iter_doc]:
                    # Extraer texto del área (acumular progreseivamente página por página en variable)
                    texto_pag = page.get_text("text", clip = area_texto) #
                    texto_docs[iter_doc] += texto_pag

        # Preguntar directorio dónde guardar archivo(s)
        dir_val = PySide6.QtWidgets.QFileDialog.getExistingDirectory(vent_princ, "Export File(s)")

        # Guardar archivos txt conservando el nombre de los archivos de referencia
        if dir_val:
            # Iterar cada archivo del diccionario
            for indice_val, doc in docs_dicc.items():
                ruta_txt = os.path.join(dir_val, f"{os.path.splitext(os.path.basename(doc.name))[0]}.txt")

                try:
                    with open(ruta_txt, 'w', encoding='utf-8') as f:
                        f.write(texto_docs[indice_val])
                except Exception as e:
                    return

# Aplicar márgen a todas las pestañas
def aplicar_margen_pestanas():
    global margen_bool

    margen_bool = not margen_bool # Invertir el valor del bool

# VENTANAS
# Ventana de rango de páginas
def ventana_rango_paginas():
    global pags_inicio, pags_fin

    ventana = rango_paginas.rango_paginas_ui() # Crear la ventana (no visible aún)
    ventana.ventana_ui() # Configurar la interfaz (añadir widgets, estilos, etc.)

    # Asignar el rango de páginas para el documento según el diccionario
    #rango_paginas.input_inicio.setValue(pags_inicio[tab_indice]) #
    #rango_paginas.input_fin.setValue(pags_fin[tab_indice]) #


    if ventana.exec() == PySide6.QtWidgets.QDialog.Accepted: # Si el usuario hizo clic en "OK"
        #pags_inicio[], pags_fin[] = ventana.obtener_rango() # Asigna los valores a las variables globales
        pass

# Ventana "Acerca de"
def ventana_acerca_de():
    ventana = acerca_de.acerca_de_ui() #

    ventana.ventana_ui() #
    ventana.exec() #

# CONEXIONES DE EVENTOS Y SEÑALES
# Conectar acciones del menú
ui_val.accion_abrir.triggered.connect(abrir_pdf) # Conecta la acción "Open" con la función "abrir_pdf"
ui_val.accion_exportar.triggered.connect(exportar_txt) # Conecta la acción "Export" con la "función exportar_txt"
ui_val.accion_aplicar_margen_todas_pestanas.triggered.connect(aplicar_margen_pestanas) # Conecta la acción "Apply Margin to All Tabs" con la función "aplicar_margen_pestanas"
ui_val.accion_rango_paginas.triggered.connect(ventana_rango_paginas) # Conecta la acción "Pages Range" con la función "ventana_rango_paginas"
ui_val.accion_acerca_de.triggered.connect(ventana_acerca_de) # Conecta la acción "About Exakova TextFlow" con la función "ventana_acerca_de"

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
