import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets

#
class rango_paginas_ui(PySide6.QtWidgets.QDialog):
    def ventana_ui(self):
        # Configuración básica de la ventana
        self.setObjectName("rango_paginas_ui")
        self.resize(300, 180)
        self.setStyleSheet("""
            background-color: #1f1f1f;
            color: white;
            font-family: 'Microsoft YaHei';
        """)
        self.setWindowTitle("Page Range Selection")
        self.setModal(True)  # Ventana modal

        # Layout principal
        self.layout_principal = PySide6.QtWidgets.QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # Título
        self.etiqueta_titulo = PySide6.QtWidgets.QLabel("Select Page Range")
        self.etiqueta_titulo.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding-bottom: 10px;
            border-bottom: 1px solid #505254;
        """)
        self.layout_principal.addWidget(self.etiqueta_titulo)

        # Contenedor para los inputs
        self.contenedor_inputs = PySide6.QtWidgets.QWidget()
        self.contenedor_inputs.setStyleSheet("background-color: #292a2b; border-radius: 4px;")
        self.layout_inputs = PySide6.QtWidgets.QFormLayout(self.contenedor_inputs)
        self.layout_inputs.setContentsMargins(15, 15, 15, 15)
        self.layout_inputs.setSpacing(10)

        # Campo página inicial
        self.input_inicio = PySide6.QtWidgets.QSpinBox()
        self.input_inicio.setRange(1, 9999)
        self.input_inicio.setStyleSheet("""
            QSpinBox {
                background-color: #1f1f1f;
                border: 1px solid #505254;
                color: white;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;  /* Elimina los botones */
            }
        """)
        self.layout_inputs.addRow("Start page:", self.input_inicio)

        # Campo página final
        self.input_fin = PySide6.QtWidgets.QSpinBox()
        self.input_fin.setRange(1, 9999)
        self.input_fin.setStyleSheet(self.input_inicio.styleSheet())
        self.layout_inputs.addRow("End page:", self.input_fin)

        self.layout_principal.addWidget(self.contenedor_inputs)

        # Contenedor botones
        self.contenedor_botones = PySide6.QtWidgets.QWidget()
        self.layout_botones = PySide6.QtWidgets.QHBoxLayout(self.contenedor_botones)
        self.layout_botones.setContentsMargins(0, 0, 0, 0)
        self.layout_botones.setSpacing(6)

        # Espaciador flexible
        self.layout_botones.addItem(PySide6.QtWidgets.QSpacerItem(
            20, 20,
            PySide6.QtWidgets.QSizePolicy.Expanding,
            PySide6.QtWidgets.QSizePolicy.Minimum
        ))

        # Botón Cancelar
        self.boton_cancelar = PySide6.QtWidgets.QPushButton("Cancel")
        self.boton_cancelar.setStyleSheet("""
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
        """)
        self.boton_cancelar.clicked.connect(self.reject)
        self.layout_botones.addWidget(self.boton_cancelar)

        # Botón Aceptar
        self.boton_aceptar = PySide6.QtWidgets.QPushButton("OK")
        self.boton_aceptar.setStyleSheet("""
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
        """)
        self.boton_aceptar.clicked.connect(self.accept)
        self.layout_botones.addWidget(self.boton_aceptar)

        self.layout_principal.addWidget(self.contenedor_botones)

        # Establecer valores por defecto
        self.input_inicio.setValue(1)
        self.input_fin.setValue(1)

    #
    def obtener_rango(self):
        # Devuelve tupla con (inicio, fin)
        return (self.input_inicio.value(), self.input_fin.value())
