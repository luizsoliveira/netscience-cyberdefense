import json
import os
import utils
from ripe_client import RIPEClient
from datetime import datetime
from math import floor, ceil
import json
import sys
import subprocess

task_working_dir = os.getcwd()
print(f" 📂 Starting task on CWD: {task_working_dir}")

today = datetime.today()
print(f" 🕣 Starting time: {today}")

file = open('task.json')
task = json.load(file)

print(f" 🔑 Task key: {task['id']}")
print(f" ⚙️ Task parameters:")
utils.print_task_parameters(task)

p = task['parameters']

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

# Preparing the parameters
collection_site = p['collection_site']

# datetime_start = datetime.strptime(p['datetime_start'], date_format) 
# datetime_end = datetime.strptime(p['datetime_end'], date_format) 
# anomalous_datetime_start = datetime.strptime(p['anomalous_datetime_start'], date_format) 
# anomalous_datetime_end = datetime.strptime(p['anomalous_datetime_end'], date_format) 

date_start = p['date_start']
date_end = p['date_end']

anomalous_date_start = p['anomalous_date_start']
anomalous_date_end = p['anomalous_date_end']

anomalous_time_start = p['anomalous_time_start']
anomalous_time_end = p['anomalous_time_end']

data_partition_training = p['data_partition_training'] 
data_partition_testing = p['data_partition_testing'] 
rnn_length = p['rnn_length']

cache = '/var/cache/ripe' if p['cache'] == 'activated' else False
debug = True if p['debug'] == 'activated' else False

#Converting parameters to the CyberDefense CMD

#CyberDefense parameters JSON
cd_json = {}

cd_json.update({"site_choice": collection_site})

cd_json.update({"start_date_key": date_start})
cd_json.update({"end_date_key": date_end})

cd_json.update({"start_date_anomaly_key": anomalous_date_start})
cd_json.update({"end_date_anomaly_key": anomalous_date_end})

cd_json.update({"start_time_anomaly_key": anomalous_time_start})
cd_json.update({"end_time_anomaly_key": anomalous_time_end})

cut_pct_key = str(floor(data_partition_training/10)) + str(ceil(data_partition_testing/10))
cd_json.update({"cut_pct_key": cut_pct_key})
cd_json.update({"rnn_seq_key": rnn_length})

filenameCD='cyberdefense_params.json'

# Writing  the CyberDefense JSON parameters file
try:
    file = open(filenameCD, 'w')
    file.write(json.dumps(cd_json,indent=2))
    file.close()
except Exception as err:
    msg=f"Failure when writing file: {filenameCD} error: {err}"
    print(msg)
    raise Exception(msg)

#Checking if the file was created

if not os.path.exists(filenameCD):
    sys.exit("ABORTING: CyberDefense parameters file is mandatory.")

fileCD = open(filenameCD)
cd_params = json.load(fileCD)
fileCD.close()

print('')

print(f" ⚙️ Parameters passed to the CyberDefense Command Line Interface:")
utils.print_generic_parameters(cd_params)

print('')

# Specify the file where you want to redirect the output
output_file = f"{task_working_dir}/stdout.log"

command = f"python3 -u cli.py -p {task_working_dir}/{filenameCD}"
command = f"{command} | tee -a {output_file}"

print(f"CWD TR: {os.getcwd()}")
print(f"Task Dir: {task_working_dir}")
print(f"Command: {command}")

# Open the file in write mode (overwriting previous content if exists)
with open(output_file, "a") as file:
    # Create a subprocess with stdout redirected to a file and tee'd to the console
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd='/usr/src/app/original/CyberDefense/'
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
print(f"CyberDefense CLI exited with return code {return_code}")

today = datetime.today()
print(f" 🕣 Ending time: {today}")

# client = RIPEClient(cacheLocation=cache, logging=False, debug=debug)
# files = client.download_updates_interval_files(datetime_start, datetime_end)

# # The timestamps are returned as they are being generated using yield
# for file in files:
#     print(file)