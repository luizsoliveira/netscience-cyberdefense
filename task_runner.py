import json
import os
import utils

print(f" 📂 Starting task on CWD: {os.getcwd()}")

file = open('task.json')
task = json.load(file)

print(f" 🔑 Task key: {task['key']}")
print(f" ⚙️ Task parameters:")
utils.print_task_parameters(task)