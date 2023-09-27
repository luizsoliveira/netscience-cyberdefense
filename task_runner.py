import json
import os
import utils
from ripe_client import RIPEClient
from datetime import datetime

print(f" 📂 Starting task on CWD: {os.getcwd()}")

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
datetime_start = datetime.strptime(p['datetime_start'], date_format) 
datetime_end = datetime.strptime(p['datetime_end'], date_format) 
anomalous_datetime_start = datetime.strptime(p['anomalous_datetime_start'], date_format) 
anomalous_datetime_end = datetime.strptime(p['anomalous_datetime_end'], date_format) 
data_partition_training = p['data_partition_training'] 
data_partition_testing = p['data_partition_testing'] 
rnn_length = p['rnn_length'] 


client = RIPEClient(cacheLocation='/var/cache/ripe', logging=False, debug=True)
#client = RIPEClient()

files = client.download_updates_interval_files(datetime_start, datetime_end)

# The timestamps are returned as they are being generated using yield
for file in files:
    print(file)