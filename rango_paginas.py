from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QWidget, QFormLayout,
    QSpinBox, QHBoxLayout, QSpacerItem, QSizePolicy,
    QPushButton, QMessageBox
)

class RangoPaginasUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Configuración básica de la ventana
        self.setObjectName("RangoPaginasUI")
        self.resize(300, 180)
        self.setWindowTitle("Page Range Selection")
        self.setModal(True)

        self.setStyleSheet("""
            background-color: #1f1f1f;
            color: white;
            font-family: 'Microsoft YaHei';
        """)

        # Layout principal
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # Título
        self.etiqueta_titulo = QLabel("Select Page Range")
        self.etiqueta_titulo.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding-bottom: 10px;
            border-bottom: 1px solid #505254;
        """)
        self.layout_principal.addWidget(self.etiqueta_titulo)

        # Contenedor para los inputs
        self.setup_inputs()

        # Contenedor para los botones
        self.setup_buttons()

        # Validación inicial
        self.validar_rango()

    def setup_inputs(self):
        self.contenedor_inputs = QWidget()
        self.contenedor_inputs.setStyleSheet("background-color: #292a2b; border-radius: 4px;")
        self.layout_inputs = QFormLayout(self.contenedor_inputs)
        self.layout_inputs.setContentsMargins(15, 15, 15, 15)
        self.layout_inputs.setSpacing(10)

        # Campo página inicial
        self.input_inicio = QSpinBox()
        self.input_inicio.setRange(1, 9999)
        self.input_inicio.setValue(1)
        self.input_inicio.setStyleSheet(self.spinbox_style())
        self.input_inicio.setToolTip("Enter the start page number")

        # Campo página final
        self.input_fin = QSpinBox()
        self.input_fin.setRange(1, 9999)
        self.input_fin.setValue(2)
        self.input_fin.setStyleSheet(self.spinbox_style())
        self.input_fin.setToolTip("Enter the end page number")

        # Agregar campos al layout
        self.layout_inputs.addRow("Start page:", self.input_inicio)
        self.layout_inputs.addRow("End page:", self.input_fin)

        # Eventos para validación en vivo
        self.input_inicio.valueChanged.connect(self.validar_rango)
        self.input_fin.valueChanged.connect(self.validar_rango)

        self.layout_principal.addWidget(self.contenedor_inputs)

    def setup_buttons(self):
        self.contenedor_botones = QWidget()
        self.layout_botones = QHBoxLayout(self.contenedor_botones)
        self.layout_botones.setContentsMargins(0, 0, 0, 0)
        self.layout_botones.setSpacing(6)

        self.layout_botones.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.boton_cancelar = QPushButton("Cancel")
        self.boton_cancelar.setStyleSheet(self.button_style("gray"))
        self.boton_cancelar.clicked.connect(self.reject)

        self.boton_aceptar = QPushButton("OK")
        self.boton_aceptar.setStyleSheet(self.button_style("blue"))
        self.boton_aceptar.clicked.connect(self.validar_y_aceptar)

        self.layout_botones.addWidget(self.boton_cancelar)
        self.layout_botones.addWidget(self.boton_aceptar)

        self.layout_principal.addWidget(self.contenedor_botones)

    def spinbox_style(self):
        return """
            QSpinBox {
                background-color: #1f1f1f;
                border: 1px solid #505254;
                color: white;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
            }
        """

    def button_style(self, color):
        if color == "gray":
            return """
                QPushButton {
                    background-color: #505254;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #606264;
                    border: 1px solid #707274;
                }
            """
        elif color == "blue":
            return """
                QPushButton {
                    background-color: #235c96;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #2c73ba;
                    border: 1px solid #50a0f0;
                }
            """

    def validar_rango(self):
        valido = self.input_inicio.value() <= self.input_fin.value()
        self.boton_aceptar.setEnabled(valido)

    def validar_y_aceptar(self):
        if self.input_inicio.value() > self.input_fin.value():
            QMessageBox.warning(self, "Invalid Range", "Start page must be less than or equal to End page.")
        else:
            self.accept()

    def obtener_rango(self):
        return self.input_inicio.value(), self.input_fin.value()
