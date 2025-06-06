from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog,
                              QGraphicsScene, QGraphicsView)
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtCore import Qt
import fitz  # PyMuPDF
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Variables de estado
        self.current_file = None
        self.doc = None

        # Conexiones de señales
        self.ui.actionOpen.triggered.connect(self.open_pdf)
        self.ui.actionExport.triggered.connect(self.export_pdf)

        # Configuración de scrollbars
        self.setup_scrollbars()

        # Configuración inicial del PDF View
        self.setup_pdf_view()

    def setup_scrollbars(self):
        """Configura la sincronización entre scrollbars"""
        # Conectar scrollbars bidireccionalmente
        self.ui.rightScrollBar.valueChanged.connect(
            lambda v: self.ui.pdfView.verticalScrollBar().setValue(v))

        self.ui.pdfView.verticalScrollBar().valueChanged.connect(
            lambda v: self.ui.rightScrollBar.setValue(v))

        # Ocultar scrollbar nativo del QGraphicsView
        self.ui.pdfView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setup_pdf_view(self):
        """Configuración inicial del visor PDF"""
        self.scene = QGraphicsScene()
        self.ui.pdfView.setScene(self.scene)
        self.ui.pdfView.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.TextAntialiasing)

    def open_pdf(self):
        """Abre diálogo para seleccionar archivo PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir PDF", "", "PDF Files (*.pdf)")

        if file_path:
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        """Carga y muestra el PDF seleccionado"""
        try:
            # Cerrar documento previo si existe
            if self.doc:
                self.doc.close()

            self.current_file = file_path
            self.doc = fitz.open(file_path)
            self.display_pdf_page(0)  # Mostrar primera página

            # Configurar scrollbar según el tamaño del documento
            self.adjust_scrollbar()

        except Exception as e:
            print(f"Error al cargar PDF: {e}")

    def display_pdf_page(self, page_num):
        """Muestra una página específica del PDF"""
        if not self.doc:
            return

        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Render a alta resolución

        # Convertir a QImage y luego a QPixmap
        image = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format_RGB888)

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(image))
        self.ui.pdfView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def adjust_scrollbar(self):
        """Ajusta la scrollbar derecha según el contenido del PDF"""
        if not self.doc:
            return

        # Calcular relación entre vista y contenido total
        view_height = self.ui.pdfView.viewport().height()
        content_height = self.scene.itemsBoundingRect().height()

        # Mostrar scrollbar solo si el contenido es más grande que la vista
        needs_scrollbar = content_height > view_height
        self.ui.rightScrollBar.setVisible(needs_scrollbar)

        if needs_scrollbar:
            # Configurar rango y paso de la scrollbar
            pdf_scrollbar = self.ui.pdfView.verticalScrollBar()
            self.ui.rightScrollBar.setRange(0, pdf_scrollbar.maximum())
            self.ui.rightScrollBar.setPageStep(pdf_scrollbar.pageStep())
            self.ui.rightScrollBar.setSingleStep(pdf_scrollbar.singleStep())

    def export_pdf(self):
        """Exporta el PDF actual (placeholder)"""
        if not self.current_file:
            return

        # Aquí iría la lógica de exportación
        print(f"Exportando {self.current_file}...")

    def resizeEvent(self, event):
        """Maneja el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        self.adjust_scrollbar()
        if self.doc:
            self.ui.pdfView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication([])

    # Necesario para PyMuPDF 1.18.0+
    import sys
    import os
    if hasattr(sys, 'frozen'):
        from PySide6.QtCore import QLibraryInfo
        os.environ["PATH"] += os.pathsep + QLibraryInfo.location(QLibraryInfo.BinariesPath)

    widget = Widget()
    widget.show()
    app.exec()
