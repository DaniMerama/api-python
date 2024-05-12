import numpy as np
from flask import Flask, jsonify, request
import uuid
import time
from datetime import datetime


try:
    tareas = np.load("tareas.data.npy", allow_pickle=True)
except:
    tareas = np.array([])

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Curso Python intermedio"


# Timestamp Endpoints


# Aqui obtenemos el tiempo de ahora mismo en numero
@app.route("/timestamp")
def get_timestamp():
    now = time.time()
    return jsonify(int(now))


# Aqui convertimos un numero a fecha
@app.route("/timestamp/print/<int:timestamp>")
def print_timestamp(timestamp):
    date_object = datetime.fromtimestamp(timestamp)
    return jsonify(date_object)


# CRUD Create Read Update Delete


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas.tolist())


# Tarea
@app.route("/tareas/<string:id_tarea>", methods=["GET"])
def obtener_tarea_por_id(id_tarea):
    respuesta = jsonify({"mensaje": "Tarea NO encontrada"})
    tarea = None
    for i in range(len(tareas)):
        item = tareas[i]

        if item["id"] == uuid.UUID(id_tarea):
            tarea = item
            break
    if tarea:
        respuesta = jsonify(tarea)
    return respuesta


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    global tareas
    nueva_tarea = request.json
    # Aqui esta el error
    nueva_tarea["id"] = uuid.uuid4()
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


@app.route("/tareas/<string:id_tarea>", methods=["DELETE"])
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
