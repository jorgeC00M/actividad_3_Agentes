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
    print("7. Demostración completa (1→6)")
    print("0. Salir")
    print("\n" + "-" * 60)


def ejecutar_simulacion(numero: int):
    if numero == 1:
        simular_ejercicio1()
    elif numero == 2:
        simular_ejercicio2()
    elif numero == 3:
        simular_ejercicio3()
    elif numero == 4:
        simular_ejercicio4()
    elif numero == 5:
        simular_ejercicio5()
    elif numero == 6:
        simular_ejercicio6()
    elif numero == 7:
        print("\n=== DEMOSTRACIÓN COMPLETA: EJERCICIOS 1 AL 6 ===\n")
        simular_ejercicio1()
        simular_ejercicio2()
        simular_ejercicio3()
        simular_ejercicio4()
        simular_ejercicio5()
        simular_ejercicio6()
    else:
        print("Opción no válida.")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-7): ").strip()

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


if __name__ == "__main__":
    main()
