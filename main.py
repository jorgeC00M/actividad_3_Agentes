# main.py
"""
Menú principal para ejecutar las simulaciones de agentes con interfaz gráfica.

Ejecutar desde la raíz del proyecto:
    python main.py
"""

from src.interfaz.ui_ejercicio1 import lanzar_ui_ejercicio1
from src.interfaz.ui_ejercicio2 import lanzar_ui_ejercicio2
from src.interfaz.ui_ejercicio3 import lanzar_ui_ejercicio3
from src.interfaz.ui_ejercicio4 import lanzar_ui_ejercicio4
from src.interfaz.ui_ejercicio5 import lanzar_ui_ejercicio5
from src.interfaz.ui_ejercicio6 import lanzar_ui_ejercicio6


def mostrar_menu():
    print("\n" + "=" * 60)
    print("        SISTEMA DE SIMULACIÓN BASADA EN AGENTES")
    print("                 ACTIVIDAD 3 - TALLER")
    print("=" * 60)
    print("\nEJERCICIOS DISPONIBLES (INTERFAZ GRÁFICA):")
    print("1. Agente limpiador con memoria (sin repetir celdas)")
    print("2. Tipos de suciedad con distintos valores")
    print("3. Agente que detecta y evita obstáculos (replanificación)")
    print("4. Comunicación entre agentes recolectores")
    print("5. Agente que aprende áreas con más comida (memoria espacial)")
    print("6. Sistema competitivo por recursos limitados")
    print("0. Salir")
    print("\n" + "-" * 60)


def ejecutar_opcion(opcion: int):
    if opcion == 1:
        lanzar_ui_ejercicio1()
    elif opcion == 2:
        lanzar_ui_ejercicio2()
    elif opcion == 3:
        lanzar_ui_ejercicio3()
    elif opcion == 4:
        lanzar_ui_ejercicio4()
    elif opcion == 5:
        lanzar_ui_ejercicio5()
    elif opcion == 6:
        lanzar_ui_ejercicio6()
    else:
        print("Opción no válida.")


def main():
    while True:
        mostrar_menu()
        op = input("Seleccione una opción (0-6): ").strip()

        if op == "0":
            print("\n¡Gracias por usar el sistema de simulación!")
            break

        if op in [str(i) for i in range(1, 7)]:
            ejecutar_opcion(int(op))
        else:
            print("Opción no válida. Por favor seleccione 0-6.")


if __name__ == "__main__":
    main()
