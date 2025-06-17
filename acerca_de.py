import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets

class acerca_de_ui(PySide6.QtWidgets.QDialog):
    def ventana_ui(self):
        # Configuración básica de la ventana
        self.setObjectName("acerca_de_ui")
        self.resize(240, 240)
        self.setStyleSheet("background-color: rgb(31, 31, 31);")
        self.setWindowTitle("About Exakova TextFlow") # Texto traducido

        # Layout principal
        self.layout_vertical = PySide6.QtWidgets.QVBoxLayout(self)
        self.layout_vertical.setSpacing(10) # Espacio entre widgets
        self.layout_vertical.setContentsMargins(30, 30, 30, 30) # Márgenes: izquierda, arriba, derecha, abajo

        # Etiqueta principal
        self.texto_principal = PySide6.QtWidgets.QLabel(self)
        self.texto_principal.setObjectName("texto_principal")
        self.texto_principal.setStyleSheet("color: white;")
        self.texto_principal.setAlignment(PySide6.QtCore.Qt.AlignLeading | PySide6.QtCore.Qt.AlignLeft | PySide6.QtCore.Qt.AlignTop)
        self.texto_principal.setWordWrap(True) # Ajuste de texto
        self.texto_principal.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Minimum)

        fuente_principal = PySide6.QtGui.QFont()
        fuente_principal.setFamily("Microsoft YaHei")
        fuente_principal.setPointSize(11)
        fuente_principal.setBold(True)
        self.texto_principal.setFont(fuente_principal)
        self.texto_principal.setText("Exakova TextFlow") # Mantenido igual por ser nombre de producto

        # Etiqueta secundaria
        self.texto_secundario = PySide6.QtWidgets.QLabel(self)
        self.texto_secundario.setObjectName("texto_secundario")
        self.texto_secundario.setStyleSheet("color: white;")
        self.texto_secundario.setAlignment(PySide6.QtCore.Qt.AlignLeading | PySide6.QtCore.Qt.AlignLeft | PySide6.QtCore.Qt.AlignTop)
        self.texto_secundario.setWordWrap(True)
        self.texto_secundario.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Expanding, PySide6.QtWidgets.QSizePolicy.Minimum)
        self.texto_secundario.setOpenExternalLinks(True) # Permite abrir enlaces

        fuente_secundaria = PySide6.QtGui.QFont()
        fuente_secundaria.setFamily("Microsoft YaHei")
        fuente_secundaria.setPointSize(8)
        fuente_secundaria.setBold(False)
        self.texto_secundario.setFont(fuente_secundaria)
        self.texto_secundario.setText("""
        <html><head/><body>
        <p>Version 1.0</p>
        <p>Copyright© 2025 Exakova Inc.</p>
        <p>All rights reserved</p>
        <p>Web: <a href="https://github.com/exakova" style="color: #007BFF; text-decoration: underline;">https://github.com/exakova</a></p>
        <p>Email: <a href="mailto:exakova@protonmail.com" style="color: #007BFF; text-decoration: underline;">exakova@protonmail.com</a></p>
        </body></html>
        """)

        # Espaciador
        self.espaciador_vertical = PySide6.QtWidgets.QSpacerItem(20, 40, PySide6.QtWidgets.QSizePolicy.Minimum, PySide6.QtWidgets.QSizePolicy.Expanding)

        # Añadir widgets al layout
        self.layout_vertical.addWidget(self.texto_principal)
        self.layout_vertical.addWidget(self.texto_secundario)
        self.layout_vertical.addItem(self.espaciador_vertical)

        # Configurar tamaño fijo
        self.setFixedSize(self.size())
        self.setSizeGripEnabled(False) # Deshabilita el redimensionamiento
