import numpy as np
from flask import Flask, jsonify, request

tareas = []
try:
    print("Try")
    tareas = np.load("tareas.data.npy", allow_pickle=True)
    print(tareas)
except:
    print("Execept")
    tareas = np.array([])

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Curso Python intermedio"


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas.tolist())


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    global tareas
    nueva_tarea = request.json
    nueva_tarea["id"] = len(tareas) + 1
    tareas = np.append(tareas, nueva_tarea)
    np.save("tareas.data", tareas)
    return jsonify({"mensaje": "Tarea creada con éxito"})


if __name__ == "__main__":
    app.run()
