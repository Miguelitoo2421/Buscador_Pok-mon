import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from ui import PokemonApp
from pokemon_api import fetch_pokemon_data, fetch_pokemon_list
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar la fuente desde la carpeta 'fonts'
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Hey Comic.ttf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))  # Establecer la fuente para toda la aplicación
    else:
        print("No se pudo cargar la fuente.")

    # Pasar la función que obtiene los datos de la API
    window = PokemonApp(fetch_pokemon_data, fetch_pokemon_list)
    window.show()

    sys.exit(app.exec())
