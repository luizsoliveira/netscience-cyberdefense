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

print(" ⏰ Waiting 10s due to time to PostgREST start")
time.sleep(10)

client = NetScienceClient(base_url='http://postgrest:3000', username='luizsoliveira@gmail.com', password='123456', logging=False)
counter=0

print(" 🚚 Task catcher service started. ")

while True:
    task = client.catch_task('BGPAnomaly')
    
    if (task):
        print(" ✅ New task found.")
        task_working_dir = f"/var/tasks/{task['id']}"

        stdout_path = f"{task_working_dir}/stdout.log"
        print(f" ✅ Writing output in: {stdout_path}")

        # Executing python script without stdout buffer
        command = "python3 -u /usr/src/app/task_runner.py"

        # Specify the file where you want to redirect the output
        output_file = f"{task_working_dir}/stdout.log"

        # Open the file in write mode (overwriting previous content if exists)
        with open(output_file, "w") as file:
            # Create a subprocess with stdout redirected to a file and tee'd to the console
            process = subprocess.Popen(
                f"{command} | tee -a {output_file}",
                shell=True,
                stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=task_working_dir
            )

            # Read and print the output in real-time
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line, end="")

        # Wait for the subprocess to complete
        process.wait()

        # Optionally, you can check the return code of the subprocess
        return_code = process.returncode
        print(f"Subprocess exited with return code {return_code}")
        updated = client.update_task_finished(task, return_code)
        if updated:
            print(f"Task {updated['id']} finished_at attribute updated {updated['finished_at']}")

    #else:
    #    print(f" 🕣  No pending tasks found. Checking again in {INTERVAL_DURING_TASK_CATCHING} seconds.")
    
    time.sleep(INTERVAL_DURING_TASK_CATCHING)
    






