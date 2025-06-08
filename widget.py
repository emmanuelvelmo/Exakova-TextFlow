import sys
import os
import PySide6.QtWidgets
import PySide6.QtGui
import PySide6.QtCore
import ui_form
import fitz

class PDFViewer(PySide6.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ui_form.Ui_Widget()
        self.ui.setupUi(self)

        # Variables de estado
        self.current_file = None
        self.doc = None
        self.docs = {}
        self.page_items = []
        self.page_spacing = 10

        # Configuración inicial
        self.setup_ui()
        self.setup_scrollbars()
        self.setup_pdf_view()
        self.setup_tab_bar()

    def setup_ui(self):
        self.ui.actionOpen.triggered.connect(self.open_pdf)
        self.ui.actionExport.triggered.connect(self.export_pdf)
        self.ui.actionApply_Margin_to_All_Tabs.triggered.connect(self.toggle_margin_action)

    def toggle_margin_action(self):
        current_text = self.ui.actionApply_Margin_to_All_Tabs.text()
        if "✔" in current_text:
            self.ui.actionApply_Margin_to_All_Tabs.setText("Apply Margin to All Tabs")
        else:
            self.ui.actionApply_Margin_to_All_Tabs.setText("Apply Margin to All Tabs")

        # Aquí puedes agregar la lógica para aplicar/remover los márgenes
        print(f"Apply Margin to All Tabs: {'✔' in current_text}")

    def setup_tab_bar(self):
        self.ui.tabBar.tabCloseRequested.connect(self.close_tab)
        self.ui.tabBar.currentChanged.connect(self.tab_changed)

        style = """
            QTabBar::close-button {
                subcontrol-origin: padding;
                subcontrol-position: right;
                width: 16px;
                height: 16px;
                margin-right: 2px;
            }
            QTabBar::close-button:hover {
                background: #505254;
                border-radius: 2px;
            }
        """

        self.ui.tabBar.setStyleSheet(self.ui.tabBar.styleSheet() + style)

    def tab_changed(self, index):
        if index >= 0 and index in self.docs:
            self.doc = self.docs[index]
            self.current_file = self.doc.name
            self.display_pdf_pages()
            self.adjust_scrollbar()
            self.center_first_page()

    def center_first_page(self):
        if not self.page_items:
            return

        PySide6.QtCore.QTimer.singleShot(50, lambda: self.ui.pdfView.fitInView(
            self.page_items[0],
            PySide6.QtCore.Qt.KeepAspectRatio
        ))

    def close_tab(self, index):
        if index in self.docs:
            self.docs[index].close()
            del self.docs[index]

        self.ui.tabBar.removeTab(index)

        if self.ui.tabBar.count() == 0:
            self.clear_pdf_view()
            self.current_file = None
            self.doc = None

    def setup_scrollbars(self):
        self.ui.verticalScrollBar.valueChanged.connect(self.scroll_pdf_view)
        self.ui.pdfView.verticalScrollBar().valueChanged.connect(
            lambda v: self.ui.verticalScrollBar.setValue(v))
        self.ui.pdfView.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.pdfView.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff)

    def scroll_pdf_view(self, value):
        self.ui.pdfView.verticalScrollBar().setValue(value)

    def setup_pdf_view(self):
        self.scene = PySide6.QtWidgets.QGraphicsScene()
        self.ui.pdfView.setScene(self.scene)
        self.ui.pdfView.setRenderHints(
            PySide6.QtGui.QPainter.Antialiasing |
            PySide6.QtGui.QPainter.SmoothPixmapTransform |
            PySide6.QtGui.QPainter.TextAntialiasing)
        self.ui.pdfView.setAlignment(PySide6.QtCore.Qt.AlignCenter)

    def clear_pdf_view(self):
        self.scene.clear()
        self.page_items = []
        self.ui.verticalScrollBar.setVisible(False)

    def open_pdf(self):
        file_paths, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
            self, "Abrir PDF(s)", "", "PDF Files (*.pdf)")

        if file_paths:
            for file_path in file_paths:
                self.load_pdf(file_path)

    def load_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            tab_index = self.ui.tabBar.addTab(os.path.basename(file_path))
            self.docs[tab_index] = doc

            # Configurar botón de cierre con ❌
            close_button = PySide6.QtWidgets.QPushButton("❌")
            close_button.setStyleSheet("""
                QPushButton {
                    color: white;
                    border: none;
                    padding: 0px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background: #505254;
                    border-radius: 2px;
                }
            """)
            close_button.setFixedSize(16, 16)
            self.ui.tabBar.setTabButton(tab_index, PySide6.QtWidgets.QTabBar.RightSide, close_button)

            self.ui.tabBar.setCurrentIndex(tab_index)
            self.doc = doc
            self.current_file = file_path
            self.display_pdf_pages()
            self.adjust_scrollbar()
            self.center_first_page()

        except Exception as e:
            print(f"Error al cargar PDF: {e}")

    def display_pdf_pages(self):
        if not self.doc:
            return

        self.clear_pdf_view()
        y_pos = 0

        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            image = PySide6.QtGui.QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                PySide6.QtGui.QImage.Format_RGB888)

            pixmap = PySide6.QtGui.QPixmap.fromImage(image)
            item = PySide6.QtWidgets.QGraphicsPixmapItem(pixmap)
            item.setPos(0, y_pos)
            self.scene.addItem(item)
            self.page_items.append(item)

            y_pos += pixmap.height() + self.page_spacing

        if self.page_items:
            total_height = y_pos - self.page_spacing
            self.scene.setSceneRect(PySide6.QtCore.QRectF(0, 0, self.page_items[0].pixmap().width(), total_height))

    def adjust_scrollbar(self):
        if not self.doc or not self.page_items:
            self.ui.verticalScrollBar.setVisible(False)
            return

        view_height = self.ui.pdfView.viewport().height()
        content_height = self.scene.sceneRect().height()
        needs_scrollbar = content_height > view_height

        self.ui.verticalScrollBar.setVisible(needs_scrollbar)

        if needs_scrollbar:
            pdf_scrollbar = self.ui.pdfView.verticalScrollBar()
            self.ui.verticalScrollBar.setRange(0, pdf_scrollbar.maximum())
            self.ui.verticalScrollBar.setPageStep(pdf_scrollbar.pageStep())
            self.ui.verticalScrollBar.setSingleStep(pdf_scrollbar.singleStep())

            visible_ratio = view_height / content_height
            handle_size = max(20, int(self.ui.verticalScrollBar.height() * visible_ratio))
            self.ui.verticalScrollBar.setStyleSheet(f"""
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
            """)

    def export_pdf(self):
        if not self.current_file:
            return
        print(f"Exportando {self.current_file}...")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_scrollbar()
        if self.doc and self.page_items:
            view_width = self.ui.pdfView.viewport().width()
            for item in self.page_items:
                if item.pixmap().width() > view_width:
                    self.ui.pdfView.fitInView(item, PySide6.QtCore.Qt.KeepAspectRatio)
                    break

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)

    if hasattr(sys, 'frozen'):
        os.environ["PATH"] += os.pathsep + PySide6.QtCore.QLibraryInfo.location(PySide6.QtCore.QLibraryInfo.BinariesPath)

    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())
