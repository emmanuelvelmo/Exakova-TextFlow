import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog,
                              QGraphicsScene, QGraphicsView)
from PySide6.QtGui import QImage, QPixmap, QPainter, QMouseEvent
from PySide6.QtCore import Qt, QPoint, QLibraryInfo
import fitz  # PyMuPDF
from ui_form import Ui_Widget

class PDFViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Variables de estado
        self.current_file = None
        self.doc = None
        self.dragging_label = None
        self.label_1_pos = QPoint(0, 0)
        self.label_2_pos = QPoint(0, self.ui.leftPanel.height() - 16)

        # Configuración inicial
        self.setup_ui()
        self.setup_scrollbars()
        self.setup_pdf_view()
        self.setup_label_drag()

    def setup_ui(self):
        """Configuración inicial de la interfaz"""
        self.ui.actionOpen.triggered.connect(self.open_pdf)
        self.ui.actionExport.triggered.connect(self.export_pdf)

        # Ya no conectamos los botones pushButton y pushButton_2 a nada
        # self.ui.pushButton.clicked.connect(self.add_tab)
        # self.ui.pushButton_2.clicked.connect(self.remove_tab)

        # Posicionar labels inicialmente
        self.ui.label_1.move(self.label_1_pos)
        self.ui.label_2.move(self.label_2_pos)

    def setup_scrollbars(self):
        """Configura la sincronización entre scrollbars"""
        self.ui.verticalScrollBar.valueChanged.connect(
            lambda v: self.ui.pdfView.verticalScrollBar().setValue(v))
        self.ui.pdfView.verticalScrollBar().valueChanged.connect(
            lambda v: self.ui.verticalScrollBar.setValue(v))
        self.ui.pdfView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setup_pdf_view(self):
        """Configuración inicial del visor PDF"""
        self.scene = QGraphicsScene()
        self.ui.pdfView.setScene(self.scene)
        self.ui.pdfView.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.TextAntialiasing)

    def setup_label_drag(self):
        """Configura el arrastre de los labels"""
        self.ui.label_1.installEventFilter(self)
        self.ui.label_2.installEventFilter(self)

    def eventFilter(self, source, event):
        """Maneja el arrastre de los labels"""
        if event.type() == QMouseEvent.MouseButtonPress:
            if source in [self.ui.label_1, self.ui.label_2]:
                self.dragging_label = source
                return True

        elif event.type() == QMouseEvent.MouseMove and self.dragging_label:
            y_pos = event.pos().y()
            panel_height = self.ui.leftPanel.height()

            if self.dragging_label == self.ui.label_1:
                max_y = self.ui.label_2.y() - self.ui.label_1.height()
                y_pos = max(0, min(y_pos, max_y))
                self.label_1_pos.setY(y_pos)
            else:  # label_2
                min_y = self.ui.label_1.y() + self.ui.label_1.height()
                y_pos = max(min_y, min(y_pos, panel_height - self.ui.label_2.height()))
                self.label_2_pos.setY(y_pos)

            self.dragging_label.move(self.dragging_label.x(), y_pos)
            return True

        elif event.type() == QMouseEvent.MouseButtonRelease:
            self.dragging_label = None
            return True

        return super().eventFilter(source, event)

    def open_pdf(self):
        """Abre diálogo para seleccionar archivo PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir PDF", "", "PDF Files (*.pdf)")

        if file_path:
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        """Carga y muestra el PDF seleccionado"""
        try:
            if self.doc:
                self.doc.close()

            self.current_file = file_path
            self.doc = fitz.open(file_path)
            self.display_pdf_page(0)
            self.adjust_scrollbar()

        except Exception as e:
            print(f"Error al cargar PDF: {e}")

    def display_pdf_page(self, page_num):
        """Muestra una página específica del PDF"""
        if not self.doc:
            return

        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
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

        view_height = self.ui.pdfView.viewport().height()
        content_height = self.scene.itemsBoundingRect().height()
        needs_scrollbar = content_height > view_height

        self.ui.verticalScrollBar.setVisible(needs_scrollbar)

        if needs_scrollbar:
            pdf_scrollbar = self.ui.pdfView.verticalScrollBar()
            self.ui.verticalScrollBar.setRange(0, pdf_scrollbar.maximum())
            self.ui.verticalScrollBar.setPageStep(pdf_scrollbar.pageStep())
            self.ui.verticalScrollBar.setSingleStep(pdf_scrollbar.singleStep())

    def export_pdf(self):
        """Exporta el PDF actual (placeholder)"""
        if not self.current_file:
            return
        print(f"Exportando {self.current_file}...")

    def resizeEvent(self, event):
        """Maneja el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        self.adjust_scrollbar()
        if self.doc:
            self.ui.pdfView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        # Actualizar posición de label_2 al redimensionar
        self.label_2_pos.setY(self.ui.leftPanel.height() - 16)
        self.ui.label_2.move(self.label_2_pos)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configuración necesaria para PyMuPDF
    if hasattr(sys, 'frozen'):
        os.environ["PATH"] += os.pathsep + QLibraryInfo.location(QLibraryInfo.BinariesPath)

    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())
