"""
Menú principal para ejecutar las simulaciones de agentes
"""

import os
import sys


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("        SISTEMA DE SIMULACIÓN BASADA EN AGENTES")
    print("                 ACTIVIDAD 3 - TALLER")
    print("="*60)
    print("\nEJERCICIOS DISPONIBLES:")
    print("1. Agente limpiador con memoria de lugares visitados")
    print("2. Diferentes tipos de suciedad con distintos valores") 
    print("3. Agente que evita obstáculos fijos en el entorno")
    print("4. Comunicación entre agentes recolectores")
    print("5. Agente que aprende áreas con más comida")
    print("6. Sistema donde agentes compiten por recursos limitados")
    print("7. Demostración completa (todos los ejercicios)")
    print("0. Salir")
    print("\n" + "-"*60)


def ejecutar_simulacion(numero):
    """Ejecuta la simulación correspondiente al número"""
    simulaciones = {
        1: "sim_ejercicio1.py",
        2: "sim_ejercicio2.py", 
        3: "sim_ejercicio3.py",
        4: "sim_ejercicio4.py",
        5: "sim_ejercicio5.py",
        6: "sim_ejercicio6.py",
        7: "sim_completa.py"
    }
    
    if numero in simulaciones:
        archivo = simulaciones[numero]
        ruta = os.path.join("simulaciones", archivo)
        
        if os.path.exists(ruta):
            print(f"\nEjecutando {archivo}...")
            print("-" * 40)
            os.system(f"python {ruta}")
        else:
            print(f"Error: No se encontró el archivo {ruta}")
    else:
        print("Opción no válida")


def main():
    """Función principal del menú"""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (0-7): ").strip()
            
            if opcion == '0':
                print("\n¡Gracias por usar el sistema de simulación!")
                break
            elif opcion in ['1', '2', '3', '4', '5', '6', '7']:
                ejecutar_simulacion(int(opcion))
                
                # Preguntar si desea continuar
                continuar = input("\n¿Desea ejecutar otra simulación? (s/n): ").strip().lower()
                if continuar != 's':
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
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src") or not os.path.exists("simulaciones"):
        print("Error: Ejecute este script desde el directorio raíz del proyecto")
        print("Directorio actual:", os.getcwd())
        sys.exit(1)
    
    main()