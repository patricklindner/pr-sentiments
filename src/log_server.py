from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "s3cret"
socketio = SocketIO(app)

progresses = {}
total_map = {}


@app.post("/progress/<task_name>/<total>")
def initialize_task(task_name, total):
    progresses[task_name] = 0
    total_map[task_name] = int(total)
    print(f"Created task {task_name}")
    return f"created task {task_name}"


@app.put("/progress/<task_name>")
def update(task_name):
    progresses[task_name] += 1
    print(f"Update task {task_name} to {progresses[task_name]}")
    socketio.emit("update-progress", {"task_name": task_name, "iteration": progresses[task_name]})
    return f"Updated task {task_name} to {progresses[task_name]}"


@app.get("/progress")
def get_progress():
    return render_template("progress.html", bars=progresses, total=total_map)


if __name__ == "__main__":
    socketio.run(app)
