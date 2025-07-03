from cx_Freeze import setup, Executable

setup(
    name="Exakova TextFlow",
    executables=[Executable("widget.py", base="Win32GUI")],
    options={
        "build_exe": {
            "packages": ["PySide6"],
            "excludes": ["tkinter", "unittest", "test"],
            "include_files": [
                "acerca_de.ui",
                "form.ui", 
                "rango_paginas.ui"
            ],
            "optimize": 1
        }
    }
)