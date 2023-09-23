from netscience_client import NetScienceClient
import logging
import time

INTERVAL_DURING_TASK_CATCHING=10

#Configuração de LOGGING
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
    tasks = client.catch_task('BGPAnomaly')
    counter +=1

    if (len(tasks) > 0):
        task = tasks[0]
        print(f" ✅ New tasks found.")
        print(task)
    else:
        print(f" 🕣 No pending tasks found. Checking again in {INTERVAL_DURING_TASK_CATCHING} seconds.")
    
    time.sleep(INTERVAL_DURING_TASK_CATCHING)
    






