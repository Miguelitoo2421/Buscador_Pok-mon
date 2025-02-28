import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel
from unittest.mock import Mock
from ui import PokemonApp

def mock_fetch_data(pokemon_name):
    if pokemon_name == "pikachu":
        return {
            'name': 'pikachu',
            'type': ['electric'],
            'abilities': ['static', 'lightning-rod'],
            'stats': {'hp': 35, 'attack': 55, 'defense': 40},
            'image': 'https://example.com/pikachu.png'
        }
    return None

def test_on_search_button_click_valid_data(qtbot):
    app = PokemonApp(mock_fetch_data, lambda: [])
    qtbot.addWidget(app)
    
    # Ingresar "pikachu" y hacer clic en el botón de búsqueda
    app.pokemon_name_input.setText("pikachu")
    qtbot.mouseClick(app.search_button, Qt.MouseButton.LeftButton)
    
    # Verificar que se muestra la información de Pikachu
    assert "Nombre: pikachu" in app.result_label.text()
    assert "Tipo: electric" in app.result_label.text()

def test_on_search_button_click_invalid_data(qtbot):
    app = PokemonApp(mock_fetch_data, lambda: [])
    qtbot.addWidget(app)
    
    # Ingresar un Pokémon no válido
    app.pokemon_name_input.setText("invalidpokemon")
    qtbot.mouseClick(app.search_button, Qt.MouseButton.LeftButton)
    
    # Verificar que muestra el mensaje de "Pokémon no encontrado"
    assert "Pokémon no encontrado." in app.result_label.text()

def test_show_pokeball_image(qtbot):
    app = PokemonApp(mock_fetch_data, lambda: [])
    qtbot.addWidget(app)
    
    # Verificar que la imagen de la Pokébola se muestra por defecto
    app.show_pokeball_image()
    assert app.pokemon_image_label.pixmap() is not None  # Asegurarse de que la imagen no es None
