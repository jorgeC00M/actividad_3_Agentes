"""
Menú principal para ejecutar las simulaciones.
"""

import sys
import os


def limpiar_pantalla():
    """Limpia la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal."""
    limpiar_pantalla()
    print("\n" + "=" * 70)
    print("ACTIVIDAD 3 - PROGRAMACIÓN BASADA EN AGENTES")
    print("Taller de Simulación de Sistemas")
    print("=" * 70)
    print("\n📋 EJERCICIOS DISPONIBLES:\n")
    print("  1. Ejercicio 1: Agente limpiador con memoria")
    print("  2. Ejercicio 2: Tipos de suciedad con diferentes valores")
    print("  3. Ejercicio 3: Evitación de obstáculos")
    print("  4. Ejercicio 4: Comunicación entre agentes")
    print("  5. Ejercicio 5: Memoria espacial y aprendizaje")
    print("  6. Ejercicio 6: Sistema competitivo")
    print("  7. Demo completa (todos los ejercicios)")
    print("  0. Salir")
    print("\n" + "=" * 70)


def ejecutar_simulacion(opcion: int):
    """
    Ejecuta la simulación seleccionada.
    
    Args:
        opcion: Número de opción seleccionada
    """
    simulaciones = {
        1: "simulaciones.sim_ejercicio1",
        2: "simulaciones.sim_ejercicio2",
        3: "simulaciones.sim_ejercicio3",
        4: "simulaciones.sim_ejercicio4",
        5: "simulaciones.sim_ejercicio5",
        6: "simulaciones.sim_ejercicio6",
        7: "simulaciones.sim_completa"
    }
    
    if opcion in simulaciones:
        try:
            modulo = __import__(simulaciones[opcion], fromlist=[''])
            
            # Ejecutar la función principal del módulo
            if opcion == 7:
                modulo.ejecutar_demo_completa()
            else:
                funcion_nombre = f"simular_ejercicio{opcion}"
                if hasattr(modulo, funcion_nombre):
                    getattr(modulo, funcion_nombre)()
            
            input("\n\nPresiona Enter para volver al menú...")
        except ImportError as e:
            print(f"\n❌ Error al importar el módulo: {e}")
            input("\nPresiona Enter para continuar...")
        except Exception as e:
            print(f"\n❌ Error durante la simulación: {e}")
            import traceback
            traceback.print_exc()
            input("\nPresiona Enter para continuar...")
    else:
        print("\n❌ Opción no válida")
        input("\nPresiona Enter para continuar...")


def main():
    """Función principal del programa."""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n👉 Selecciona una opción: ")
            opcion = int(opcion)
            
            if opcion == 0:
                print("\n👋 ¡Hasta luego!")
                break
            
            ejecutar_simulacion(opcion)
            
        except ValueError:
            print("\n❌ Por favor ingresa un número válido")
            input("\nPresiona Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()