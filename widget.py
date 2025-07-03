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
aplicacion_val = PySide6.QtWidgets.QApplication(sys.argv) # Crea la aplicación Qt

if hasattr(sys, 'frozen'): # Si la aplicación está compilada (ejecutable)
    os.environ["PATH"] += os.pathsep + PySide6.QtCore.QLibraryInfo.location(PySide6.QtCore.QLibraryInfo.BinariesPath) # Añade binarios Qt al PATH

# Crear el widget principal
vent_princ = PySide6.QtWidgets.QWidget() # Crea el widget principal de la aplicación

ui_val = ui_form.Ui_Widget() # Crea instancia de la interfaz de usuario
ui_val.iniciar_ui(vent_princ) # Configura la interfaz en el widget principal

# VARIABLES
# Variables para redimensionar
altura_panel_izquierdo = 1 # Altura inicial del panel izquierdo
extremo_etiqueta_1 = {} # Extremo superior del panel izquierdo (el mismo que el borde superior de la etiqueta)
extremo_etiqueta_2 = {} # Extremo inferior del panel izquierdo (el mismo que el borde inferior de la etiqueta)

# Variables de rango de páginas
pags_inicio_export = {} # Páginas de inicio para exportación por pestaña
pags_fin_export = {} # Páginas de fin para exportación por pestaña
pags_inicio_estatico = {} # Páginas de inicio estáticas por pestaña
pags_fin_estatico = {} # Páginas de fin estáticas por pestaña
frac_pag = 0 # Fracción de página para cálculos de scroll
altura_etiqueta_scroll = 4 # Altura mínima de la etiqueta de scroll

# Variables de margenes
margen_bool = True # Bandera para aplicar márgenes a todas las pestañas
margenes_superiores = {} # Márgenes superiores por pestaña
margenes_inferiores = {} # Márgenes inferiores por pestaña

# Variables para el control de la barra de desplazamiento vertical
pag_actual = {} # La página en la que nos encontramos en cada pestaña
num_pags = {} # Número de páginas por pestaña

# Múltiples eventos
indice_actual = 0 # Pestaña en la que se encuentra el usuario

# Variables para manejo de archivos
directorio_archivo = None # Archivo PDF actualmente abierto
doc_actual = None # Documento PDF actual
docs_dicc = {} # Diccionario que almacena todos los documentos abiertos por índice de tab
paginas_contenedor = [] # Lista de elementos gráficos de páginas PDF
rutas_docs = {} # Rutas de documentos por índice de pestaña

# CONFIGURACIÓN DE LA INTERFAZ DE USUARIO
# Ocultar controles para el documento
def ocultar_controles():
    ui_val.panel_derecho.setVisible(False) # Ocultar la barra scroll
    ui_val.etiqueta_scroll.setVisible(False) # Ocultar handler para barra scroll
    ui_val.panel_izquierdo.hide() # Ocultar panel izquierdo
    ui_val.etiqueta_1.hide() # Ocultar etiquetas arrastrables
    ui_val.etiqueta_2.hide() # Ocultar etiquetas arrastrables
    ui_val.area_1.hide() # Ocultar área de selección superior
    ui_val.area_2.hide() # Ocultar área de selección inferior

# Mostrar controles para el documento
def mostrar_controles():
    ui_val.panel_izquierdo.show() # Mostrar panel izquierdo
    ui_val.etiqueta_1.show() # Mostrar etiquetas arrastrables
    ui_val.etiqueta_2.show() # Mostrar etiquetas arrastrables
    ui_val.area_1.show() # Mostrar área de selección superior
    ui_val.area_2.show() # Mostrar área de selección inferior

    # Establece posiciones de etiquetas y áreas de selección
    ui_val.etiqueta_1.move(0, 0) # Posicionar etiqueta 1 en la parte superior
    ui_val.etiqueta_2.move(0, ui_val.visor_pdf.height() - ui_val.etiqueta_2.height()) # Posicionar etiqueta 2 en la parte inferior

    # Configurar geometría de las áreas de selección
    ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

# Ajustar tamaño de handler y salto de página en panel derecho
def ajustar_handler():
    global frac_pag, altura_etiqueta_scroll, indice_actual

    # Ajustar barra scroll si está habilitada
    if ui_val.panel_derecho.isVisible():
        # Píxeles de desplazamiento para una página respecto a la altura de scrollbar
        if ui_val.visor_pdf.height() / num_pags[indice_actual] < 1:
            frac_pag = (ui_val.visor_pdf.height() - altura_etiqueta_scroll) / num_pags[indice_actual]
        else:
            frac_pag = ui_val.visor_pdf.height() / num_pags[indice_actual]

        # Asignar altura en píxeles a handler según la situación
        if frac_pag <= altura_etiqueta_scroll:
            ui_val.etiqueta_scroll.setGeometry(PySide6.QtCore.QRect(0, 0, 16, altura_etiqueta_scroll)) # Altura mínima de 4 para handler
        else:
            ui_val.etiqueta_scroll.setGeometry(PySide6.QtCore.QRect(0, 0, 16, round(frac_pag))) # Altura calculada según fracción

# Recargar documento
def recargar_documento():
    global rutas_docs, indice_actual, doc_actual, directorio_archivo

    if doc_actual:
        doc_tmp = fitz.open(rutas_docs[indice_actual]) # Cargar el mismo archivo de la pestaña

        doc_actual = doc_tmp # Actualiza el documento actual
        directorio_archivo = rutas_docs[indice_actual] # Actualiza el archivo actual

        limpiar_vista_pdf() # Limpiar visor PDF

        ventana_paginas_pdf(indice_actual) # Mostrar documento

# Calcular dimensiones de elementos
def renderizar_etiquetas_areas():
    global altura_panel_izquierdo

    # Colocar etiquetas arrastrables a los extremos superior e inferior de la ventana
    ui_val.etiqueta_1.move(0, 0) # Colocar en la parte superior
    ui_val.etiqueta_2.move(0, ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height()) # Colocar en la parte inferior

    # Expandir áreas de selección horizontalmente
    ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
    ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

    # Captura de dimensiones
    altura_panel_izquierdo = ui_val.panel_izquierdo.height() # Altura inicial del panel izquierdo

# Realizar dibujado y después calcular dimensiones
PySide6.QtCore.QTimer.singleShot(0, renderizar_etiquetas_areas) # Ejecutar renderizado después del dibujado inicial

# Configurar escena gráfica para PDF
escena = PySide6.QtWidgets.QGraphicsScene() # Crea nueva escena gráfica

ui_val.visor_pdf.setScene(escena) # Asigna la escena a la vista PDF
ui_val.visor_pdf.setRenderHints(PySide6.QtGui.QPainter.Antialiasing | PySide6.QtGui.QPainter.SmoothPixmapTransform | PySide6.QtGui.QPainter.TextAntialiasing) # Configura renderizado de alta calidad

# FUNCIONES DE MANEJO DE ARCHIVOS
# Carga un archivo PDF en una nueva pestaña
def cargar_pdf(archivo_dir_tmp):
    global doc_actual, docs_dicc, directorio_archivo, pags_inicio_export, pags_fin_export, margenes_superiores, margenes_inferiores, margen_bool, extremo_etiqueta_1, extremo_etiqueta_2, altura_panel_izquierdo # Declara variables globales que se modificarán

    try:
        doc_tmp = fitz.open(archivo_dir_tmp) # Abre el archivo PDF con PyMuPDF en memoria

        # El archivo no se encuentra previamente cargado
        if os.path.basename(archivo_dir_tmp) not in [os.path.basename(doc_iter.name) for doc_iter in docs_dicc.values()]:
            indice_carg = ui_val.barra_pestanas.addTab(os.path.basename(archivo_dir_tmp)) # Añade nueva pestaña con nombre del archivo

            docs_dicc[indice_carg] = doc_tmp # Almacena el documento en el diccionario

            doc_actual = doc_tmp # Actualiza el documento actual
            directorio_archivo = archivo_dir_tmp # Actualiza el archivo actual

            # Agregar rango de páginas del documento al diccionario (valores por defecto)
            pags_inicio_export[indice_carg] = 1 # Primera página
            pags_fin_export[indice_carg] = len(doc_actual) # Asignar el número total de páginas del documento

            pags_inicio_estatico[indice_carg] = 1 # Primera página estática
            pags_fin_estatico[indice_carg] = len(doc_actual) # Última página estática

            extremo_etiqueta_1[indice_carg] = 0 # Extremo superior inicial
            extremo_etiqueta_2[indice_carg] = ui_val.visor_pdf.height() # Extremo inferior inicial

            # Establecer valores para márgenes
            if margen_bool and len(docs_dicc) > 1: # Usar los valores de la pestaña anterior
                margenes_superiores[indice_carg] = margenes_superiores[indice_carg - 1] # Copiar margen superior anterior
                margenes_inferiores[indice_carg] = margenes_inferiores[indice_carg - 1] # Copiar margen inferior anterior
            else: # Usar valores por defecto
                margenes_superiores[indice_carg] = ui_val.etiqueta_1.height() # Margen superior por defecto
                margenes_inferiores[indice_carg] = ui_val.visor_pdf.height() - ui_val.etiqueta_2.height() # Margen inferior por defecto

            # Última página vista en el documento
            pag_actual[indice_carg] = 0 # Página inicial

            # Guardar ruta en el diccionario
            rutas_docs[indice_carg] = archivo_dir_tmp

            # Mostrar controles si es el primer documento
            if len(docs_dicc) == 1:
                mostrar_controles()

            ui_val.barra_pestanas.setCurrentIndex(indice_carg) # Cambia al tab recién creado

            ventana_paginas_pdf(indice_carg) # Muestra las páginas del PDF
    except Exception as e:
        pass # Manejo silencioso de errores

# FUNCIONES DE INTERFAZ
# Maneja el evento de redimensionamiento de la ventana
def evento_redimensionamiento(evento):
    global altura_panel_izquierdo, extremo_etiqueta_1, extremo_etiqueta_2, num_pags, indice_actual, margenes_superiores, margenes_inferiores, docs_dicc

    # Procesar redimensionamiento si hay documento activo
    if doc_actual:
        # Calcular ratio del panel izquierdo después de redimensionar
        ratio_panel_izquierdo = ui_val.panel_izquierdo.height() / altura_panel_izquierdo

        # Calcular valores para márgenes en diccionarios de todas las pestañas (se actualizan oculto)
        for iter_doc in docs_dicc:
            # Normalización de posiciones de etiquetas según el caso
            norm_extremo_etiqueta_1 = round(ratio_panel_izquierdo * extremo_etiqueta_1[iter_doc])
            norm_extremo_etiqueta_2 = round(ratio_panel_izquierdo * extremo_etiqueta_2[iter_doc]) - ui_val.etiqueta_2.height()

            # Posiciones hipotéticas de las etiquetas de cada pestaña (actualiza las posiciones ciclicamente)
            pos_etiqueta_1 = margenes_superiores[iter_doc] - ui_val.etiqueta_1.height()
            pos_etiqueta_2 = margenes_inferiores[iter_doc]

            # Límites y colisiones para las etiquetas
            et_h_1 = max(0, min(norm_extremo_etiqueta_1, pos_etiqueta_2 - ui_val.etiqueta_1.height()))
            et_h_2 = min(ui_val.panel_izquierdo.height() - ui_val.etiqueta_2.height(), max(norm_extremo_etiqueta_2, pos_etiqueta_1 + ui_val.etiqueta_1.height()))

            # Actualizar valores de margenes según nueva proporción
            margenes_superiores[iter_doc] = et_h_1 + ui_val.etiqueta_1.height()
            margenes_inferiores[iter_doc] = et_h_2

        # Elementos en Visor PDF en índice actual (lo que ve el usuario)
        # Desplazar etiquetas según el ratio del panel izquierdo calculado
        ui_val.etiqueta_1.move(0, margenes_superiores[indice_actual] - ui_val.etiqueta_1.height())
        ui_val.etiqueta_2.move(0, margenes_inferiores[indice_actual])

        # Mover áreas selección a la par con las etiquetas
        ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
        ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

        # Recargar documento
        recargar_documento()

        # Ajustar handler si aplica
        ajustar_handler()

# Limpia la vista del PDF y reinicia los elementos relacionados
def limpiar_vista_pdf():
    global paginas_contenedor # Declara variable global que se modificará

    escena.clear() # Limpia todos los elementos de la escena
    paginas_contenedor = [] # Reinicia la lista de páginas

# Maneja el cambio de pestaña en la interfaz
def cambiar_pestana(indice_tab):
    global doc_actual, directorio_archivo, indice_actual, docs_dicc, margenes_superiores, margenes_inferiores, frac_pag, pag_actual # Declara variables globales que se modificarán

    if indice_tab in docs_dicc: # Verifica que el índice sea válido y exista en docs_dicc
        doc_actual = docs_dicc[indice_tab] # Cambia al documento del tab seleccionado
        directorio_archivo = doc_actual.name # Actualiza el archivo actual

        limpiar_vista_pdf() # Limpiar visor PDF

        ventana_paginas_pdf(indice_tab) # Muestra las páginas del nuevo documento

        # Cambiar de posición las etiquetas arrastrables y sus áreas
        if not margen_bool:
            ui_val.etiqueta_1.move(0, margenes_superiores[indice_tab] - ui_val.etiqueta_1.height())
            ui_val.etiqueta_2.move(0, margenes_inferiores[indice_tab])

            ui_val.area_1.setGeometry(0, 0, ui_val.visor_pdf.width(), ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height())
            ui_val.area_2.setGeometry(0, ui_val.etiqueta_2.y(), ui_val.visor_pdf.width(), ui_val.visor_pdf.height() - ui_val.etiqueta_2.y())

        # Ajustar tamaño para handler de la barra de desplazamiento
        ajustar_handler()

        # Actualizar posición del handler
        ui_val.etiqueta_scroll.move(0, round(frac_pag * pag_actual[indice_actual] - 1))

# Cierra una pestaña abierta y gestiona los recursos asociados
def cerrar_pestana(indice_val):
    global directorio_archivo, doc_actual, docs_dicc, pags_inicio_export, pags_fin_export, pags_inicio_estatico, pags_fin_estatico, margenes_superiores, margenes_inferiores, pag_actual, num_pags, rutas_docs, extremo_etiqueta_1, extremo_etiqueta_2 # Declara variables globales que se modificarán

    docs_dicc[indice_val].close() # Cierra el documento

    # Eliminar datos asociados al documento en todos los diccionarios
    del docs_dicc[indice_val] # Elimina el documento del diccionario de documentos
    del pags_inicio_export[indice_val] # Elimina páginas de inicio de exportación
    del pags_fin_export[indice_val] # Elimina páginas de fin de exportación
    del pags_inicio_estatico[indice_val] # Elimina páginas de inicio estáticas
    del pags_fin_estatico[indice_val] # Elimina páginas de fin estáticas
    del margenes_superiores[indice_val] # Elimina margen superior
    del margenes_inferiores[indice_val] # Elimina margen inferior
    del pag_actual[indice_val] # Elimina página actual
    del num_pags[indice_val] # Elimina número de páginas
    del rutas_docs[indice_val] # Elimina ruta del documento
    del extremo_etiqueta_1[indice_val] # Elimina extremo de etiqueta 1
    del extremo_etiqueta_2[indice_val] # Elimina extremo de etiqueta 2

    # Restar una posición a las claves de los diccionarios a partir del índice más uno
    docs_dicc = {i: v for i, (_, v) in enumerate(sorted(docs_dicc.items()))}
    pags_inicio_export = {i: v for i, (_, v) in enumerate(sorted(pags_inicio_export.items()))}
    pags_fin_export = {i: v for i, (_, v) in enumerate(sorted(pags_fin_export.items()))}
    pags_inicio_estatico = {i: v for i, (_, v) in enumerate(sorted(pags_inicio_export.items()))}
    pags_fin_estatico = {i: v for i, (_, v) in enumerate(sorted(pags_fin_export.items()))}
    margenes_superiores = {i: v for i, (_, v) in enumerate(sorted(margenes_superiores.items()))}
    margenes_inferiores = {i: v for i, (_, v) in enumerate(sorted(margenes_inferiores.items()))}
    pag_actual = {i: v for i, (_, v) in enumerate(sorted(pag_actual.items()))}
    num_pags = {i: v for i, (_, v) in enumerate(sorted(num_pags.items()))}
    rutas_docs = {i: v for i, (_, v) in enumerate(sorted(rutas_docs.items()))}
    extremo_etiqueta_1 = {i: v for i, (_, v) in enumerate(sorted(extremo_etiqueta_1.items()))}
    extremo_etiqueta_2 = {i: v for i, (_, v) in enumerate(sorted(extremo_etiqueta_2.items()))}

    ui_val.barra_pestanas.removeTab(indice_val) # Remueve el tab de la barra

    if ui_val.barra_pestanas.count() == 0: # Si no quedan tabs abiertos
        limpiar_vista_pdf() # Limpia la vista PDF

        # Ocultar controles
        ocultar_controles()

        directorio_archivo = None # Reinicia el archivo actual
        doc_actual = None # Reinicia el documento actual

# Renderiza y muestra las páginas del PDF en la vista
def ventana_paginas_pdf(indice_val):
    global paginas_contenedor, num_pags, pag_actual, indice_actual

    if doc_actual:
        y_pos = 0 # Posición vertical inicial

        indice_actual = indice_val # Actualizar índice de documento

        # Obtener el número de páginas y almacenarlo en el diccionario
        num_pags[indice_val] = len(doc_actual)

        # Obtener dimensiones del viewport
        viewport_altura = ui_val.visor_pdf.viewport().height()
        viewport_ancho = ui_val.visor_pdf.viewport().width()

        # Renderizar cada página del documento
        for pag_num in range(num_pags[indice_val]): # Usar el valor del diccionario
            pagina = doc_actual.load_page(pag_num) # Cargar página del documento
            pag_rect = pagina.rect # Obtener rectángulo de la página
            pag_ancho = pag_rect.width # Ancho de la página
            pag_altura = pag_rect.height # Altura de la página

            # Calcular factor de escala para ajustar la página al viewport
            factor_escala = viewport_altura / pag_altura
            if (pag_ancho * factor_escala) > viewport_ancho:
                factor_escala = viewport_ancho / pag_ancho

            # Crear matriz de transformación y renderizar página
            matriz = fitz.Matrix(factor_escala, factor_escala)
            pix = pagina.get_pixmap(matrix=matriz) # Obtener pixmap de la página
            imagen = PySide6.QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, PySide6.QtGui.QImage.Format_RGB888)
            pixmap = PySide6.QtGui.QPixmap.fromImage(imagen) # Convertir a pixmap
            item = PySide6.QtWidgets.QGraphicsPixmapItem(pixmap) # Crear item gráfico
            item.setPos(0, y_pos) # Posicionar item en la escena
            escena.addItem(item) # Agregar item a la escena
            paginas_contenedor.append(item) # Agregar item al contenedor
            y_pos += pixmap.height() # Actualizar posición vertical

        # Configurar la escena si hay páginas renderizadas
        if paginas_contenedor:
            altura_total = y_pos
            escena.setSceneRect(PySide6.QtCore.QRectF(0, 0, paginas_contenedor[0].pixmap().width(), altura_total)) # Establecer rectángulo de la escena
            ui_val.visor_pdf.fitInView(paginas_contenedor[pag_actual[indice_actual]], PySide6.QtCore.Qt.KeepAspectRatio) # Ajustar vista a la página actual

        # Verificar si hay más de una página en el diccionario
        if num_pags[indice_val] > 1:
            configurar_barra_desp(indice_val) # Configurar barra de desplazamiento

            # Permitir el desplazamiento con la voluta sobre las áreas de visión del PDF
            ui_val.visor_pdf.wheelEvent = voluta_desp
            ui_val.area_1.wheelEvent = voluta_desp
            ui_val.area_2.wheelEvent = voluta_desp

# CONFIGURACIONES PERSONALIZADAS
# Comportamiento de voluta del mouse
def voluta_desp(evento):
    global pag_actual, indice_actual, frac_pag, num_pags

    # Obtener la barra de desplazamiento vertical
    barra_scroll = ui_val.visor_pdf.verticalScrollBar()

    # Determinar la dirección del scroll (positivo = abajo, negativo = arriba)
    delta = evento.angleDelta().y()

    # Procesar scroll hacia arriba
    if delta > 0: # Scroll hacia arriba
        # Actualiza página actual en documento
        pag_actual[indice_actual] = max(0, pag_actual[indice_actual] - 1) # Página anterior sin ir debajo de 0

        # Recargar la página
        recargar_documento()

        # Actualizar posición del handler
        ui_val.etiqueta_scroll.move(0, round(frac_pag * pag_actual[indice_actual] - 1))
    else: # Scroll hacia abajo
        # Actualiza página actual en documento
        pag_actual[indice_actual] = min(num_pags[indice_actual] - 1, pag_actual[indice_actual] + 1) # Página siguiente sin exceder el límite

        # Recargar la página
        recargar_documento()

        # Actualizar posición del handler
        ui_val.etiqueta_scroll.move(0, round(frac_pag * pag_actual[indice_actual] - 1))

    evento.accept() # Aceptar el evento

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
        global altura_panel_izquierdo, extremo_etiqueta_1, extremo_etiqueta_2, margen_bool

        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Presionar botón izquierdo
            # Actualizar altura de panel izquierdo
            altura_panel_izquierdo = ui_val.panel_izquierdo.height()

            # Aplicar ratio de proporción a diccionario de extremos de etiquetas (actualizar extremos)
            if not margen_bool:
                for iter_doc in docs_dicc:
                    extremo_etiqueta_1[iter_doc] = margenes_superiores[iter_doc] - ui_val.etiqueta_1.height()
                    extremo_etiqueta_2[iter_doc] = margenes_inferiores[iter_doc] + ui_val.etiqueta_2.height()

            # Posición del click
            posicion = evento.position().toPoint()

            # Detectar cual etiqueta fue clickeada
            for etiqueta in [ui_val.etiqueta_1, ui_val.etiqueta_2]:
                if etiqueta.geometry().contains(posicion): # Si click está en etiqueta
                    datos_arrastre['arrastrando'] = True # Activar arrastre
                    datos_arrastre['etiqueta_actual'] = etiqueta # Guardar referencia
                    datos_arrastre['desfase_val'] = posicion.y() - etiqueta.y() # Calcular desfase
                    datos_arrastre['posicion_inicial_y'] = etiqueta.y() # Guardar posición inicial

                    break

            evento.accept() # Aceptar el evento

    # Maneja el evento de movimiento del ratón para arrastrar etiquetas
    def evento_mover_raton(evento):
        global extremo_etiqueta_1, extremo_etiqueta_2, indice_actual, margenes_superiores, margenes_inferiores

        if datos_arrastre['arrastrando'] and datos_arrastre['etiqueta_actual']:
            etiqueta = datos_arrastre['etiqueta_actual'] # Etiqueta siendo arrastrada
            posicion = evento.position().toPoint() # Posición actual del mouse

            tmp_y = posicion.y() - datos_arrastre['desfase_val'] # Nueva posición Y (actualización constante)

            if etiqueta == ui_val.etiqueta_1: # Para etiqueta superior
                tmp_y = max(0, min(tmp_y, ui_val.etiqueta_2.y() - etiqueta.height())) # Límites

                ui_val.area_1.setGeometry(0, 0, ui_val.area_1.width(), tmp_y + etiqueta.height()) # Redimensionar área superior según posición de etiqueta

                # Actualizar márgenes según el caso
                if margen_bool: # Si está activado aplicar márgenes a todas las pestañas
                    # Iterar todos los márgenes
                    for iter_val in margenes_superiores: # Afecta a todas las pestañas
                        margenes_superiores[iter_val] = tmp_y + ui_val.etiqueta_1.height() # Actualizar margen superior

                        extremo_etiqueta_1[iter_val] = tmp_y # Actualizar extremo superior
                        extremo_etiqueta_2[iter_val] = ui_val.etiqueta_2.y() + ui_val.etiqueta_2.height() # Actualizar extremo inferior
                else: # Afecta solo a la pestaña actual
                    margenes_superiores[indice_actual] = tmp_y + ui_val.etiqueta_1.height() # Actualizar margen superior de pestaña actual

                    extremo_etiqueta_1[indice_actual] = tmp_y # Actualizar extremo superior de pestaña actual
                    extremo_etiqueta_2[indice_actual] = ui_val.etiqueta_2.y() + ui_val.etiqueta_2.height() # Actualizar extremo inferior de pestaña actual

            else: # Para etiqueta inferior
                tmp_y = max(ui_val.etiqueta_1.y() + ui_val.etiqueta_1.height(), min(tmp_y, ui_val.panel_izquierdo.height() - etiqueta.height())) # Aplicar límites de posición

                ui_val.area_2.setGeometry(0, tmp_y, ui_val.area_2.width(), vent_princ.height() - tmp_y - ui_val.barra_menu.height() - ui_val.barra_pestanas.height()) # Redimensionar área inferior según posición de etiqueta

                # Actualizar márgenes según el caso
                if margen_bool: # Si está activado aplicar márgenes a todas las pestañas
                    # Iterar todos los márgenes
                    for iter_val in margenes_inferiores: # Afecta a todas las pestañas
                        margenes_inferiores[iter_val] = tmp_y # Actualizar margen inferior

                        extremo_etiqueta_2[iter_val] = tmp_y + ui_val.etiqueta_2.height() # Actualizar extremo inferior
                        extremo_etiqueta_1[iter_val] = ui_val.etiqueta_1.y() # Actualizar extremo superior
                else: # Afecta solo a la pestaña actual
                    margenes_inferiores[indice_actual] = tmp_y # Actualizar margen inferior de pestaña actual

                    extremo_etiqueta_2[indice_actual] = tmp_y + ui_val.etiqueta_2.height() # Actualizar extremo inferior de pestaña actual
                    extremo_etiqueta_1[indice_actual] = ui_val.etiqueta_1.y() # Actualizar extremo superior de pestaña actual

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

# Comportamiento de scrollbar
def configurar_barra_desp(indice_val):
    global num_pags, frac_pag

    # Diccionario para mantener el estado del scroll
    barra_scroll_presionada = False # Estado inicial de variable (botón izquierdo no presionado)

    # Mostrar la barra scroll y handler
    ui_val.panel_derecho.setVisible(True) # Hacer visible el panel derecho
    ui_val.etiqueta_scroll.setVisible(True) # Hacer visible la etiqueta de scroll

    # Ajustar tamaño para handler de la barra de desplazamiento y salto de página
    ajustar_handler() # Llamar función para ajustar dimensiones

    # Al presionar sobre el scroll
    def evento_presion_barra_scroll(evento):
        nonlocal barra_scroll_presionada
        global pag_actual, paginas_contenedor

        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Si se presiona botón izquierdo
            barra_scroll_presionada = True # Actualizar estado de variable

            # Obtener posición del cursor
            pos_cursor = evento.position().toPoint() # Convertir posición a punto

            # Obtener número de página en base a altura del cursor
            pos_pag = int(pos_cursor.y() / frac_pag) # Calcular página según fracción

            # Cambiar página si aplica
            if pag_actual[indice_val] != pos_pag: # Si la página es diferente a la actual
                # Cambiar a nueva página
                ui_val.visor_pdf.centerOn(paginas_contenedor[pos_pag]) # Centrar vista en nueva página

                # Actualizar página actual
                pag_actual[indice_val] = pos_pag # Guardar nueva página actual

                # Mover handler a posición
                ui_val.etiqueta_scroll.move(0, round(frac_pag * pag_actual[indice_actual] - 1)) # Actualizar posición del handler

            evento.accept() # Aceptar el evento

    # Al mover la barra de scroll
    def evento_mover_barra_scroll(evento):
        nonlocal barra_scroll_presionada
        global pag_actual, paginas_contenedor

        # Se presiona el handler
        if barra_scroll_presionada: # Si está presionado el botón
            # Obtener posición del cursor continuamente (while implícito)
            pos_cursor = evento.position().toPoint() # Convertir posición a punto

            # Obtener número de página en base a altura del cursor
            pos_pag = int(pos_cursor.y() / frac_pag) # Calcular página según fracción

            # Cambiar página si aplica
            if pag_actual[indice_val] != pos_pag: # Si la página es diferente a la actual
                # Cambiar a nueva página
                ui_val.visor_pdf.centerOn(paginas_contenedor[pos_pag]) # Centrar vista en nueva página

                # Actualizar página actual
                pag_actual[indice_val] = pos_pag # Guardar nueva página actual

                # Mover handler a posición
                ui_val.etiqueta_scroll.move(0, round(frac_pag * pag_actual[indice_actual] - 1)) # Actualizar posición del handler

            evento.accept() # Aceptar el evento

    # Soltar el botón izquierdo del mouse
    def evento_soltar_barra_scroll(evento):
        nonlocal barra_scroll_presionada

        if evento.button() == PySide6.QtCore.Qt.LeftButton: # Si se suelta botón izquierdo
            barra_scroll_presionada = False # Actualizar estado de variable

            evento.accept() # Aceptar el evento

    # Asignar los eventos personalizados al scrollbar
    ui_val.panel_derecho.mousePressEvent = evento_presion_barra_scroll # Asignar evento de presión
    ui_val.panel_derecho.mouseMoveEvent = evento_mover_barra_scroll # Asignar evento de movimiento
    ui_val.panel_derecho.mouseReleaseEvent = evento_soltar_barra_scroll # Asignar evento de liberación

# FUNCIONES DE ACCIONES
# Abre uno o varios archivos PDF mediante un cuadro de diálogo
def abrir_pdf():
    archivos_rutas, filtro_val = PySide6.QtWidgets.QFileDialog.getOpenFileNames(vent_princ, "Open PDF(s)", "", "PDF Files (*.pdf)") # Abre diálogo para seleccionar archivos PDF

    if archivos_rutas: # Si se seleccionaron archivos
        # Itera sobre cada archivo seleccionado
        for archivo_dir_tmp in archivos_rutas: # Itera sobre cada ruta seleccionada
            cargar_pdf(archivo_dir_tmp) # Carga cada archivo PDF

# Exportar texto en PDF a TXT
def exportar_txt():
    global margen_bool, texto_docs, docs_dicc, paginas_contenedor, margenes_superiores, margenes_inferiores

    # Variables
    texto_docs = {iter_doc: "" for iter_doc in docs_dicc} # Inicializar diccionario para almacenar texto de cada documento

    # Procesar si hay documentos cargados
    if docs_dicc: # Si hay documentos en el diccionario
        # Obtener altura de la primera página en píxeles (acorde a la altura del visor PDF)
        altura_pagina = paginas_contenedor[0].pixmap().height() # Altura de la primera página renderizada

        # Mismos márgenes para todas las pestañas
        if margen_bool: # Si está activado aplicar márgenes a todas las pestañas
            # Convertir la altura de los márgenes a fracción del total de la página
            extremo_y1 = margenes_superiores[0] / altura_pagina # Fracción del margen superior
            extremo_y2 = margenes_inferiores[0] / altura_pagina # Fracción del margen inferior

        # Iterar sobre cada archivo
        for iter_doc in docs_dicc: # Procesar cada documento
            # Distintos márgenes para cada pestaña
            if not margen_bool: # Si no está activado aplicar márgenes a todas las pestañas
                # Convertir la altura de los márgenes a fracción del total de la página
                extremo_y1 = margenes_superiores[iter_doc] / altura_pagina # Fracción del margen superior específico
                extremo_y2 = margenes_inferiores[iter_doc] / altura_pagina # Fracción del margen inferior específico

            # Iterar sobre el rango de páginas del archivo
            for pag_num in range(pags_inicio_export[iter_doc] - 1, pags_fin_export[iter_doc]): # Recorrer páginas en el rango
                pag_val = docs_dicc[iter_doc].load_page(pag_num) # Cargar página específica
                pag_rect = pag_val.rect # Obtener rectángulo de la página

                # Definir área de recorte
                clip_rect = fitz.Rect(0, pag_rect.height * extremo_y1, pag_rect.width, pag_rect.height * extremo_y2) # Crear rectángulo de recorte

                # Extraer texto del área definida
                bloques = pag_val.get_text("blocks", clip = clip_rect) # Obtener bloques de texto del área

                for bloque in bloques: # Procesar cada bloque de texto
                    # El índice 4 contiene el texto del bloque
                    texto_bloque = bloque[4] # Extraer texto del bloque

                    # Procesar cada línea del bloque
                    lineas = texto_bloque.split('\n') # Dividir texto en líneas
                    lineas_procesadas = [] # Lista para líneas procesadas

                    for i, linea in enumerate(lineas): # Procesar cada línea
                        linea = linea.strip() # Eliminar espacios en blanco

                        if linea: # Solo procesar líneas con contenido
                            # Manejar guiones al final de línea
                            if linea.endswith('-') and i < len(lineas) - 1 and lineas[i + 1]: # Si línea termina en guión y hay siguiente línea
                                linea = linea[: - 1] + lineas[i + 1].lstrip() # Unir con siguiente línea
                                lineas[i + 1] = '' # Marcar la siguiente línea como ya procesada

                            lineas_procesadas.append(linea) # Agregar línea procesada

                    # Unir líneas procesadas con espacios
                    parrafo = ' '.join([linea for linea in lineas_procesadas if linea]) # Crear párrafo uniendo líneas

                    # Agregar doble salto de línea entre párrafos
                    if parrafo: # Si hay contenido en el párrafo
                        texto_docs[iter_doc] += parrafo + '\n\n' # Agregar párrafo con saltos de línea

            if len(texto_docs[iter_doc].splitlines()) > 1: # Si hay más de una línea
                texto_docs[iter_doc] = '\n'.join(texto_docs[iter_doc].splitlines()[: - 1]) # Elimina las últimas dos líneas en blanco

        # Preguntar directorio dónde guardar archivo(s)
        dir_val = PySide6.QtWidgets.QFileDialog.getExistingDirectory(vent_princ, "Export File(s)") # Mostrar diálogo para seleccionar directorio

        # Guardar archivos txt conservando el nombre de los archivos de referencia
        if dir_val: # Si se seleccionó un directorio
            for indice_val, doc_actual in docs_dicc.items(): # Iterar sobre cada documento
                ruta_txt = os.path.join(dir_val, f"{os.path.splitext(os.path.basename(doc_actual.name))[0]}.txt") # Crear ruta del archivo txt

                try:
                    with open(ruta_txt, 'w', encoding='utf-8') as f: # Abrir archivo para escritura
                        f.write(texto_docs[indice_val]) # Escribir texto al archivo
                except Exception as e:
                    pass # Manejo silencioso de errores

# Aplicar márgen a todas las pestañas
def aplicar_margen_pestanas():
    global margen_bool, indice_actual, margenes_superiores, margenes_inferiores, extremo_etiqueta_1, extremo_etiqueta_2, docs_dicc

    margen_bool = not margen_bool # Invertir el valor del bool

    # Establecer los mismos márgenes y coordenadas para los diccionarios
    if margen_bool and len(docs_dicc) > 0: # Si está activado y hay documentos
        margen_superior_tmp = margenes_superiores[indice_actual] # Obtener margen superior actual
        margen_inferior_tmp = margenes_inferiores[indice_actual] # Obtener margen inferior actual

        extremo_etiqueta_1_tmp = extremo_etiqueta_1[indice_actual] # Obtener extremo superior actual
        extremo_etiqueta_2_tmp = extremo_etiqueta_2[indice_actual] # Obtener extremo inferior actual

        # Iterar todos los márgenes y coordenadas
        for iter_doc in docs_dicc: # Aplicar a todos los documentos
            margenes_superiores[iter_doc] = margen_superior_tmp # Asignar margen superior
            margenes_inferiores[iter_doc] = margen_inferior_tmp # Asignar margen inferior

            extremo_etiqueta_1[iter_doc] = extremo_etiqueta_1_tmp # Asignar extremo superior
            extremo_etiqueta_2[iter_doc] = extremo_etiqueta_2_tmp # Asignar extremo inferior

# FUNCIONES PARA ACCESOS DIRECTOS POR TECLADO
# Cambiar a la pestaña siguiente
def cambiar_pestana_siguiente():
    global indice_actual, docs_dicc, doc_actual

    if doc_actual: # Si hay documento activo
        indice_actual += 1 # Incrementar índice

        if indice_actual > len(docs_dicc) - 1: # Si excede el límite
            indice_actual = len(docs_dicc) - 1 # Mantener en el último índice

        ui_val.barra_pestanas.setCurrentIndex(indice_actual) # Desplazarse a la pestaña siguiente

# Cambiar a la pestaña anterior
def cambiar_pestana_anterior():
    global indice_actual, doc_actual

    if doc_actual: # Si hay documento activo
        indice_actual -= 1 # Decrementar índice

        if indice_actual < 0: # Si es menor que cero
            indice_actual = 0 # Mantener en el primer índice

        ui_val.barra_pestanas.setCurrentIndex(indice_actual) # Desplazarse a la pestaña anterior

# VENTANAS
# Ventana de rango de páginas
def ventana_rango_paginas():
    global pags_inicio_export, pags_fin_export, doc_actual, indice_actual

    if doc_actual: # Si hay documento activo
        ventana = rango_paginas.rango_paginas_ui() # Crear la ventana (no visible aún)
        ventana.ventana_ui() # Configurar la interfaz (añadir widgets, estilos, etc.)

        # Asignar límites de rango seleccionables
        ventana.input_inicio.setRange(1, pags_fin_estatico[indice_actual]) # Establecer rango para página inicial
        ventana.input_fin.setRange(1, pags_fin_estatico[indice_actual]) # Establecer rango para página final

        # Asignar extremos de páginas para el documento según el diccionario
        ventana.input_inicio.setValue(pags_inicio_export[indice_actual]) # Establecer valor inicial
        ventana.input_fin.setValue(pags_fin_export[indice_actual]) # Establecer valor final

        # Captura de variables temporales (anteriores a las del usuario)
        ventana.inicio_tmp = pags_inicio_export[indice_actual] # Guardar valor temporal inicial
        ventana.fin_tmp = pags_fin_export[indice_actual] # Guardar valor temporal final

        if ventana.exec() == PySide6.QtWidgets.QDialog.Accepted: # Si el usuario hizo clic en "OK"
            pags_inicio_export[indice_actual], pags_fin_export[indice_actual] = ventana.obtener_rango() # Asigna los valores a las variables globales

# Ventana "Acerca de"
def ventana_acerca_de():
    ventana = acerca_de.acerca_de_ui() # Crear ventana acerca de

    ventana.ventana_ui() # Configurar interfaz de la ventana
    ventana.exec() # Mostrar ventana modal

# CONEXIONES DE EVENTOS Y SEÑALES
# Conectar acciones del menú
ui_val.accion_abrir.triggered.connect(abrir_pdf)  # Conecta la acción "Open" con la función "abrir_pdf"
ui_val.accion_exportar.triggered.connect(exportar_txt)  # Conecta la acción "Export" con la función "exportar_txt"
ui_val.accion_aplicar_margen_todas_pestanas.triggered.connect(aplicar_margen_pestanas)  # Conecta la acción "Apply Margin to All Tabs" con la función "aplicar_margen_pestanas"
ui_val.accion_rango_paginas.triggered.connect(ventana_rango_paginas)  # Conecta la acción "Pages Range" con la función "ventana_rango_paginas"
ui_val.accion_acerca_de.triggered.connect(ventana_acerca_de)  # Conecta la acción "About Exakova TextFlow" con la función "ventana_acerca_de"

# Conectar eventos de pestañas
ui_val.barra_pestanas.tabCloseRequested.connect(cerrar_pestana)  # Conecta la señal de cierre de tab
ui_val.barra_pestanas.currentChanged.connect(cambiar_pestana)  # Conecta la señal de cambio de tab

# Conectar evento de redimensionamiento
evento_redimen_original = vent_princ.resizeEvent  # Guarda el evento original de redimensionamiento
vent_princ.resizeEvent = lambda evento: (evento_redimen_original(evento), evento_redimensionamiento(evento))  # Combina evento original con handler personalizado

# Accesos directos con teclado
atajo_recargar_ctrl_r = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("Ctrl + R"), vent_princ) # Crear atajo Ctrl+R
atajo_recargar_ctrl_r.activated.connect(recargar_documento) # Conectar atajo con función de recarga

atajo_recargar_f5 = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("F5"), vent_princ) # Crear atajo F5
atajo_recargar_f5.activated.connect(recargar_documento) # Conectar atajo con función de recarga

atajo_pestana_siguiente = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("Ctrl + Tab"), vent_princ) # Crear atajo Ctrl+Tab
atajo_pestana_siguiente.activated.connect(cambiar_pestana_siguiente) # Conectar atajo con función de cambio

atajo_pestana_anterior = PySide6.QtGui.QShortcut(PySide6.QtGui.QKeySequence("Ctrl + Shift + Tab"), vent_princ) # Crear atajo Ctrl+Shift+Tab
atajo_pestana_anterior.activated.connect(cambiar_pestana_anterior) # Conectar atajo con función de cambio

# CONFIGURACIONES DE LA GUI
# Configurar los labels arrastrables
configurar_etiquetas_arrastrables() # Inicializar comportamiento de etiquetas arrastrables

# Ocultar controles al inicio
ocultar_controles() # Ocultar controles hasta que se abra un documento

# PUNTO DE PARTIDA DE LA APLICACIÓN
vent_princ.show() # Muestra la ventana principal
sys.exit(aplicacion_val.exec()) # Inicia el bucle de eventos y termina cuando se cierra la aplicación
