"""Utilidades de visualización."""

import os
from typing import Any, List


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_grid(
    entorno: Any,
    agentes: List[Any] = None,
    titulo: str = "",
    estadisticas: dict = None
):
    """
    Muestra el grid del entorno con información adicional.
    
    Args:
        entorno: Entorno a visualizar
        agentes: Lista de agentes
        titulo: Título a mostrar
        estadisticas: Estadísticas adicionales
    """
    if titulo:
        print(f"\n{'=' * 70}")
        print(f"{titulo:^70}")
        print('=' * 70)
    
    print()
    print(entorno.render(agentes))
    print()
    
    if estadisticas:
        print("Estadísticas:")
        for clave, valor in estadisticas.items():
            if isinstance(valor, float):
                print(f"  {clave}: {valor:.2f}")
            else:
                print(f"  {clave}: {valor}")
        print()


def crear_barra_progreso(porcentaje: float, ancho: int = 30) -> str:
    """
    Crea una barra de progreso ASCII.
    
    Args:
        porcentaje: Porcentaje de progreso (0-100)
        ancho: Ancho de la barra
        
    Returns:
        String con la barra de progreso
    """
    lleno = int(ancho * porcentaje / 100)
    vacio = ancho - lleno
    return f"[{'█' * lleno}{'░' * vacio}] {porcentaje:.1f}%"