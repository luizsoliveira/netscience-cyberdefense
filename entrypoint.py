from netscience_client import NetScienceClient
import logging
import time
import subprocess
import sys

INTERVAL_DURING_TASK_CATCHING=10

# LOGGING setup
logging.basicConfig(
    filename='netscience.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

#client = RIPEClient(cacheLocation='./cache/ripe', logging=logging)

client = NetScienceClient(base_url='http://postgrest:3000', username='luizsoliveira@gmail.com', password='123456', logging=False)
counter=0

while True:
    task = client.catch_task('BGPAnomaly')
    
    if (task):
        print(" ✅ New task found.")
        task_working_dir = f"/var/tasks/{task['key']}"

        result = subprocess.run(
            [sys.executable, "/usr/src/app/task_runner.py"],
             capture_output=True,
             cwd=task_working_dir,
             text=True
)
        print("stdout:")
        print(result.stdout)
        print("stderr:")
        print(result.stderr)

    else:
        print(f" 🕣  No pending tasks found. Checking again in {INTERVAL_DURING_TASK_CATCHING} seconds.")
    
    time.sleep(INTERVAL_DURING_TASK_CATCHING)
    






