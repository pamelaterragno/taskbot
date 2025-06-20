import os
import json

RUTA_ARCHIVO = "data/tareas.json"

def cargar_tareas():
    if not os.path.exists(RUTA_ARCHIVO):
        return {}
    with open(RUTA_ARCHIVO, "r") as f:
        return json.load(f)

def guardar_tareas(tareas):
    os.makedirs("data", exist_ok=True)
    with open(RUTA_ARCHIVO, "w") as f:
        json.dump(tareas, f, indent=2)

#Agreta tarea formato <text> #etiqueta
def agregar_tarea(user_id: str, texto: str):
    tareas = cargar_tareas()
    tareas_usuario = tareas.get(user_id, [])

    partes = texto.rsplit('#', 1)
    descripcion = partes[0].strip()
    etiqueta = partes[1].strip().lower() if len(partes) > 1 else "sin_etiqueta"

    tareas_usuario.append({
        "texto": descripcion,
        "hecha": False,
        "etiqueta": etiqueta
    })
    tareas[user_id] = tareas_usuario
    guardar_tareas(tareas)

#Muestra las tareas del usuario
def listar_tareas(user_id: str):
    tareas = cargar_tareas()
    return tareas.get(user_id, [])

#Marca una tarea como completada por id
def marcar_hecha(user_id: str, idx: int) -> bool:
    tareas = cargar_tareas()
    if user_id not in tareas or idx < 0 or idx >= len(tareas[user_id]):
        return False
    tareas[user_id][idx]["hecha"] = True
    guardar_tareas(tareas)
    return True

#Elimina tarea por id
def eliminar_tarea_por_indice(user_id: str, indice: int) -> bool:
    tareas = cargar_tareas()
    tareas_usuario = tareas.get(user_id, [])

    if 0 <= indice < len(tareas_usuario):
        del tareas_usuario[indice]
        tareas[user_id] = tareas_usuario
        guardar_tareas(tareas)
        return True

    return False

# Muestra tareas filtradas por etiqueta
def filtrar_por_etiqueta(user_id: str, etiqueta: str):
    tareas = cargar_tareas()
    tareas_usuario = tareas.get(user_id, [])
    return [t for t in tareas_usuario if t.get("etiqueta", "sin_etiqueta") == etiqueta.lower() and not t["hecha"]]

#Elimina las ultimas tareas que habían sido marcadas como completadas, pide cantidad
def eliminar_ultimas_completadas(user_id: str, cantidad: int = 1):
    tareas = cargar_tareas()
    tareas_usuario = tareas.get(user_id, [])

    # Filtrar tareas hechas con sus índices originales
    completadas = [(i, t) for i, t in enumerate(tareas_usuario) if t["hecha"]]

    if not completadas:
        return 0  # Nada para borrar

    # Tomar las últimas `cantidad` tareas completadas (desde el final)
    a_borrar = completadas[-cantidad:]
    indices_a_borrar = [i for i, _ in a_borrar]

    # Borrarlas del final hacia el principio para no romper índices
    for i in sorted(indices_a_borrar, reverse=True):
        del tareas_usuario[i]

    tareas[user_id] = tareas_usuario
    guardar_tareas(tareas)
    return len(indices_a_borrar)
