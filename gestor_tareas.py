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

def agregar_tarea(user_id: str, texto: str):
    tareas = cargar_tareas()
    tareas_usuario = tareas.get(user_id, [])
    tareas_usuario.append({"texto": texto, "hecha": False})
    tareas[user_id] = tareas_usuario
    guardar_tareas(tareas)

def listar_tareas(user_id: str):
    tareas = cargar_tareas()
    return tareas.get(user_id, [])

def marcar_hecha(user_id: str, idx: int) -> bool:
    tareas = cargar_tareas()
    if user_id not in tareas or idx < 0 or idx >= len(tareas[user_id]):
        return False
    tareas[user_id][idx]["hecha"] = True
    guardar_tareas(tareas)
    return True

