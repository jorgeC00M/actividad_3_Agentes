# main.py
"""
Menú principal para ejecutar las simulaciones de agentes.
Ejecutar desde la raíz del proyecto con:
    python main.py
"""

from simulaciones.sim_ejercicio1 import simular_ejercicio1
from simulaciones.sim_ejercicio2 import simular_ejercicio2
from simulaciones.sim_ejercicio3 import simular_ejercicio3
from simulaciones.sim_ejercicio4 import simular_ejercicio4
from simulaciones.sim_ejercicio5 import simular_ejercicio5
from simulaciones.sim_ejercicio6 import simular_ejercicio6


def mostrar_menu():
    print("\n" + "=" * 60)
    print("        SISTEMA DE SIMULACIÓN BASADA EN AGENTES")
    print("                 ACTIVIDAD 3 - TALLER")
    print("=" * 60)
    print("\nEJERCICIOS DISPONIBLES:")
    print("1. Agente limpiador con memoria (sin repetir celdas)")
    print("2. Tipos de suciedad con distintos valores")
    print("3. Agente que detecta y evita obstáculos (replanificación)")
    print("4. Comunicación entre agentes recolectores")
    print("5. Agente que aprende áreas con más comida (memoria espacial)")
    print("6. Sistema competitivo por recursos limitados")
    print("0. Salir")
    print("\n" + "-" * 60)


def ejecutar_simulacion(numero: int):
    sims = {
        1: simular_ejercicio1,
        2: simular_ejercicio2,
        3: simular_ejercicio3,
        4: simular_ejercicio4,
        5: simular_ejercicio5,
        6: simular_ejercicio6,
    }
    if numero in sims:
        print(f"\nEjecutando simulación {numero}...\n" + "-" * 40)
        sims[numero]()
    else:
        print("Opción no válida.")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-6): ").strip()

        if opcion == "0":
            print("\n¡Gracias por usar el sistema de simulación!")
            break
        if opcion in [str(i) for i in range(1, 7)]:
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
            print("Opción no válida. Por favor, seleccione 0-6.")


if __name__ == "__main__":
    main()
