from collections import deque
import heapq

tareas = [
    "Diseñar la interfaz de usuario",
    "Implementar la lógica de negocio",
    "Desarrollar la base de datos",
    "Probar la aplicación",
    "Documentar el código",
    "Implementar el sistema de seguridad",
    "Desplegar la aplicación en producción",
]

personas = [
    "Juan Pérez (Desarrollador Front-end)",
    "María Sánchez (Desarrolladora Back-end)",
    "Carlos López (Analista de Sistemas)",
    "Ana Rodríguez (Diseñadora UX/UI)",
    "Pedro Gómez (Tester)",
    "Sofía Martínez (Especialista en Seguridad)",
]

recursos = [
    "Servidor de desarrollo",
    "Base de datos PostgreSQL",
    "Herramientas de diseño Figma",
    "Entorno de pruebas virtualizado",
    "Software de documentación Sphinx",
]

MAX_RESPONSABLES = 2
MAX_TAREAS_POR_PERSONA = 3

estado_inicial = {tarea: {"responsables": [], "recurso": None} for tarea in tareas}

def es_valido(estado):
    conteo_personas = {persona: 0 for persona in personas}

    for asignacion in estado.values():
        if not asignacion["responsables"] or not asignacion["recurso"]:
            return False
        for persona in asignacion["responsables"]:
            conteo_personas[persona] += 1
            if conteo_personas[persona] > MAX_TAREAS_POR_PERSONA:
                return False
    return True

def heuristica(estado):
    return sum(1 for asignacion in estado.values() if not asignacion["responsables"] or not asignacion["recurso"])

# Algoritmo de búsqueda A* optimizado
def a_estrella():
    heap = [(heuristica(estado_inicial), 0, estado_inicial)]  # (heurística, contador, estado)
    contador = 1  # Contador único para cada estado visitado
    
    while heap:
        _, _, estado_actual = heapq.heappop(heap)
        
        if es_valido(estado_actual):
            return estado_actual
        
        for tarea in tareas:
            if estado_actual[tarea]["responsables"] and estado_actual[tarea]["recurso"]:
                continue  # Saltamos si la tarea ya tiene asignación completa
            
            for persona in personas:
                if persona in estado_actual[tarea]["responsables"]:
                    continue  # Evitamos asignar la misma persona a la misma tarea
                
                if len(estado_actual[tarea]["responsables"]) >= MAX_RESPONSABLES:
                    break  # Evitamos exceder el número máximo de responsables por tarea
                
                for recurso in recursos:
                    nuevo_estado = {
                        t: {"responsables": v["responsables"][:], "recurso": v["recurso"]}
                        for t, v in estado_actual.items()
                    }  # Copia profunda del estado
                    
                    nuevo_estado[tarea]["responsables"].append(persona)
                    nuevo_estado[tarea]["recurso"] = recurso
                    
                    heapq.heappush(heap, (heuristica(nuevo_estado), contador, nuevo_estado))
                    contador += 1

    return None

solucion = a_estrella()

if solucion:
    print("Solución encontrada:")
    for tarea, asignacion in solucion.items():
        print(f"- {tarea}:")
        print(f"  Responsables: {', '.join(asignacion['responsables'])}")
        print(f"  Recurso: {asignacion['recurso']}")
else:
    print("No se encontró una solución válida")
