# src/utils/visualizacion.py
class Visualizador:
    """Clase para visualizar entornos en consola (útil para debug)."""

    @staticmethod
    def mostrar_entorno_limpieza(entorno, agente=None):
        print(f"Tiempo: {entorno.tiempo} | Suciedad: {len(entorno.suciedad)}")
        for y in range(entorno.alto):
            fila = []
            for x in range(entorno.ancho):
                if agente and x == agente.x and y == agente.y:
                    fila.append("A")
                elif hasattr(entorno, "obstaculos") and (x, y) in entorno.obstaculos:
                    fila.append("X")
                elif hasattr(entorno, "suciedad"):
                    s = entorno.suciedad
                    if isinstance(s, dict) and (x, y) in s:
                        tipo = s[(x, y)]["tipo"]
                        fila.append(entorno.tipos_suciedad[tipo]["simbolo"])
                    elif isinstance(s, set) and (x, y) in s:
                        fila.append("*")
                    else:
                        fila.append(".")
                else:
                    fila.append(".")
            print(" ".join(fila))
        print()

    @staticmethod
    def mostrar_entorno_recoleccion(entorno, agentes=None):
        if agentes is None:
            agentes = []
        print(f"Tiempo: {entorno.tiempo} | Comida: {len(entorno.comida)}")
        for y in range(entorno.alto):
            fila = []
            for x in range(entorno.ancho):
                ag = None
                for a in agentes:
                    if a.x == x and a.y == y:
                        ag = a
                        break
                if ag:
                    fila.append(ag.id[0])
                elif (x, y) in entorno.obstaculos:
                    fila.append("X")
                elif (x, y) in entorno.comida:
                    fila.append("C")
                else:
                    fila.append(".")
            print(" ".join(fila))
        print()
