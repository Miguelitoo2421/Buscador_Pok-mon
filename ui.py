import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QListWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests

class PokemonApp(QMainWindow):
    def __init__(self, fetch_data_function, fetch_list_function):
        super().__init__()
        self.setWindowTitle("Pokémon Info")
        self.setGeometry(200, 200, 400, 400)  # Ajusta el tamaño de la ventana

        # Función que consulta los datos
        self.fetch_pokemon_data = fetch_data_function
        self.fetch_pokemon_list = fetch_list_function  # Función para obtener la lista de nombres de Pokémon

        # Crear los widgets
        self.pokemon_name_input = QLineEdit(self)
        self.pokemon_name_input.setPlaceholderText("Ingrese el nombre de un Pokémon")
        self.pokemon_name_input.textChanged.connect(self.on_text_changed)  # Detectar cambios en el texto

        self.suggestions_list = QListWidget(self)  # Lista de sugerencias
        self.suggestions_list.hide()
        self.suggestions_list.itemClicked.connect(self.on_suggestion_selected)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.on_search_button_click)

        self.result_label = QLabel("Información Pokémon.", self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokemon_image_label = QLabel(self)  # Agregar una etiqueta para la imagen

        # Crear el layout para los datos del Pokémon y la imagen
        data_layout = QVBoxLayout()
        data_layout.addWidget(self.result_label)

        image_layout = QVBoxLayout()
        image_layout.addWidget(self.pokemon_image_label)  # Agregar la etiqueta de la imagen

        # Crear un layout horizontal para colocar los datos y la imagen uno al lado del otro
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(data_layout)
        horizontal_layout.addLayout(image_layout)

        # Crear el layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.pokemon_name_input)
        
        main_layout.addWidget(self.suggestions_list)  # Agregamos la lista debajo del input
        
        main_layout.addWidget(self.search_button)
        main_layout.addLayout(horizontal_layout)  # Usar el layout horizontal para los datos e imagen

        # Crear un contenedor para la ventana
        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        # Cargar la imagen de la pokébola por defecto
        self.pokeball_image_path = os.path.join(os.path.dirname(__file__), 'images', 'pokeball.png')
        self.show_pokeball_image()

        
        # Aplicar el estilo con QSS
        self.setStyleSheet("""
                           
            QWidget {
                background-color: #EF5350;
            }
                           
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #3761A8;        
            }

            QPushButton {
                background-color: #4DAD5B;
                color: black;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-right: 100px;
                margin-left: 100px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLabel {
                font-size: 20px;
                color: black;
                margin-top: 15px;
                background-color: #FECA1B;
                padding: 20px;
                border-radius: 5px;
            }
        """)
    def show_pokeball_image(self):
        """Mostrar la imagen de la pokébola"""
        pokeball_image = QPixmap(self.pokeball_image_path)
        scaled_pokeball = pokeball_image.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.pokemon_image_label.setPixmap(scaled_pokeball)
        self.pokemon_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar la imagen

    def on_text_changed(self):
        text = self.pokemon_name_input.text().strip().lower()
        if not text:
            self.show_pokeball_image()
            self.result_label.setText("Información Pokémon.")
            self.suggestions_list.hide()
            return
        
        all_pokemon = self.fetch_pokemon_list()
        matches = [name for name in all_pokemon if text in name.lower()]
        
        self.suggestions_list.clear()
        if matches:
            self.suggestions_list.addItems(matches)
            self.suggestions_list.show()
        else:
            self.suggestions_list.hide()

    def on_search_button_click(self):
        pokemon_name = self.pokemon_name_input.text().strip()

        if pokemon_name:  # Solo buscar si el campo no está vacío
            data = self.fetch_pokemon_data(pokemon_name)

            if data:
                result_text = (
                    f"Nombre: {data['name']}\n"
                    f"Tipo: {', '.join(data['type'])}\n"
                    f"Habilidad: {', '.join(data['abilities'])}\n"
                    f"Estadísticas:\n"
                    f"{'\n'.join([f'{k}: {v}' for k, v in data['stats'].items()])}"
                )
                self.result_label.setText(result_text)

                # Descargar la imagen del Pokémon
                pokemon_image_url = data['image']
                image_data = requests.get(pokemon_image_url).content  # Descargar la imagen
                image = QPixmap()
                image.loadFromData(image_data)  # Cargar los datos de la imagen en un QPixmap

                # Escalar la imagen para que se ajuste sin distorsionar
                scaled_image = image.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)

                # Ajustar el tamaño máximo de la imagen
                max_width = 220
                max_height = 220
                scaled_image = scaled_image.scaled(min(scaled_image.width(), max_width),
                                                   min(scaled_image.height(), max_height), Qt.AspectRatioMode.KeepAspectRatio)

                self.pokemon_image_label.setPixmap(scaled_image)
                self.pokemon_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar la imagen
            else:
                self.result_label.setText("Pokémon no encontrado.")
                self.pokemon_image_label.clear()  # Limpiar la imagen si no se encuentra el Pokémon
        else:
            self.show_pokeball_image()  # Volver a mostrar la pokébola si el campo está vacío
            self.result_label.clear()  # Limpiar los datos si no se ha buscado un Pokémon
            self.result_label.setText("Ingrese un nombre Pokémon.")
            
    def on_suggestion_selected(self, item):
        """Maneja la selección de un elemento de la lista de sugerencias"""
        self.pokemon_name_input.setText(item.text())
        self.suggestions_list.hide()