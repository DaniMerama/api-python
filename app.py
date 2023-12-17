import numpy as np
from flask import Flask, jsonify, request

try:
    tareas = np.load("tareas.data.npy", allow_pickle=True)
except:
    tareas = np.array([])

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Curso Python intermedio"


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas.tolist())


# Tarea
@app.route("/tareas/<int:id_tarea>", methods=["GET"])
def obtener_tarea_por_id(id_tarea):
    # Completar lógica para que regrese solo la tarea con el ID
    # si no existe regresar Tarea NO encontrada
    return True


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    global tareas
    nueva_tarea = request.json
    nueva_tarea["id"] = len(tareas) + 1
    tareas = np.append(tareas, nueva_tarea)
    np.save("tareas.data", tareas)
    return jsonify({"mensaje": "Tarea creada con éxito"})


@app.route("/tareas", methods=["PUT"])
def actualizar_tarea():
    global tareas
    tarea_actualizada = request.json
    bandera = False
    respuesta = jsonify({"mensaje": "Tarea NO encontrada"})
    for i in range(len(tareas)):
        item = tareas[i]
        if item["id"] == tarea_actualizada["id"]:
            tareas[i] = tarea_actualizada
            np.save("tareas.data", tareas)
            bandera = True
            break
    if bandera:
        respuesta = jsonify({"mensaje": "Tarea actualizada con éxito"})

    return respuesta


@app.route("/tareas/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    global tareas
    bandera = False
    respuesta = jsonify({"mensaje": "Tarea NO encontrada"})
    for i in range(len(tareas)):
        item = tareas[i]
        if item["id"] == id_tarea:
            tareas = np.delete(tareas, i)
            np.save("tareas.data", tareas)
            bandera = True
            break
    if bandera:
        respuesta = jsonify({"mensaje": "Tarea eliminada con éxito"})

    return respuesta


if __name__ == "__main__":
    app.run()
