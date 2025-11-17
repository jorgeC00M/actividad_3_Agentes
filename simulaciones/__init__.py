# simulaciones/__init__.py
import sys
import os

# Agregar el directorio raíz al path de Python
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)