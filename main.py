# main.py
"""
Menú principal para ejecutar las simulaciones de agentes.
Ejecutar desde la raíz del proyecto con:
    python main.py
"""

import sys

from simulaciones.sim_ejercicio1 import simular_ejercicio1
from simulaciones.sim_ejercicio2 import simular_ejercicio2
from simulaciones.sim_ejercicio3 import simular_ejercicio3
from simulaciones.sim_ejercicio4 import simular_ejercicio4
from simulaciones.sim_ejercicio5 import simular_ejercicio5
from simulaciones.sim_ejercicio6 import simular_ejercicio6
from simulaciones.sim_completa import demo_rapida_ejercicios


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("        SISTEMA DE SIMULACIÓN BASADA EN AGENTES")
    print("                 ACTIVIDAD 3 - TALLER")
    print("=" * 60)
    print("\nEJERCICIOS DISPONIBLES:")
    print("1. Agente limpiador con memoria de lugares visitados")
    print("2. Diferentes tipos de suciedad con distintos valores")
    print("3. Agente que evita obstáculos fijos en el entorno")
    print("4. Comunicación entre agentes recolectores")
    print("5. Agente que aprende áreas con más comida")
    print("6. Sistema donde agentes compiten por recursos limitados")
    print("7. Demostración completa (todos los ejercicios)")
    print("0. Salir")
    print("\n" + "-" * 60)


def ejecutar_simulacion(numero: int):
    """Ejecuta la simulación correspondiente al número."""
    simulaciones = {
        1: simular_ejercicio1,
        2: simular_ejercicio2,
        3: simular_ejercicio3,
        4: simular_ejercicio4,
        5: simular_ejercicio5,
        6: simular_ejercicio6,
        7: demo_rapida_ejercicios,
    }

    if numero in simulaciones:
        print(f"\nEjecutando simulación {numero}...\n" + "-" * 40)
        simulaciones[numero]()
    else:
        print("Opción no válida")


def main():
    """Función principal del menú."""
    while True:
        mostrar_menu()

        try:
            opcion = input("\nSeleccione una opción (0-7): ").strip()

            if opcion == "0":
                print("\n¡Gracias por usar el sistema de simulación!")
                break
            if opcion in [str(i) for i in range(1, 8)]:
                ejecutar_simulacion(int(opcion))

                continuar = (
                    input("\n¿Desea ejecutar otra simulación? (s/n): ")
                    .strip()
                    .lower()
                )
                if continuar != "s":
                    print("\n¡Hasta pronto!")
                    break
            else:
                print("Opción no válida. Por favor, seleccione 0-7.")

        except KeyboardInterrupt:
            print("\n\nEjecución interrumpida por el usuario.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Por favor, intente nuevamente.")


if __name__ == "__main__":
    main()
