import requests
import json
from datetime import datetime

server_address = 'http://localhost:8080/'
address_task_1 = server_address + 'Europe/Moscow'
address_task_2 = server_address + 'api/v1/convert'
address_task_3 = server_address + 'api/v1/datediff'

current_time = str(datetime.now())

task_2_data = json.dumps(
    {"date": {"date": "12.20.2021 22:21:05",
              "tz": "Europe/Moscow"},
     "target_tz": "Iran"}
)

task_3_data_1 = json.dumps(
    {"first_date": "12.20.2021 12:00:00",
     "first_tz": "Europe/Moscow",
     "second_date": "12.20.2021 12:00:00",
     "second_tz": "Iran"}
)

task_3_data_2 = json.dumps(
    {"first_date": current_time,
     "first_tz": "Asia/Tomsk",
     "second_date": "07.09.1998 13:45:00",
     "second_tz": "Asia/Irkutsk"}
)

task_3_data_3 = json.dumps(
    {"first_date": "12.20.2021 12:00:00",
     "first_tz": "Iran",
     "second_date": "12.20.2021 12:00:00",
     "second_tz": "UTC"}
)

task_3_data_bad = json.dumps(
    {"first_date": "12.20.2021 12:00:00",
     "first_tz": "wrong time zone",
     "second_date": "12.20.2021 12:00:00",
     "second_tz": "UTC"}
)

response1 = requests.get(address_task_1)
print(f'Task 1 : {response1.text}')

response2 = requests.post(address_task_2, json=task_2_data)
print(f'Task 2 : {response2.text}')

response_3_1 = requests.post(address_task_3, json=task_3_data_1)
print(f'Task 3 : {response_3_1.text}')

text = "I ve already lived for"
response_3_2 = requests.post(address_task_3, json=task_3_data_2)
print(f'{text} : {response_3_2.text} seconds')

response_3_3 = requests.post(address_task_3, json=task_3_data_3)
print(f'Task 3 : {response_3_3.text}')

print('Bad data exeption:')
response_3_4 = requests.post(address_task_3, json=task_3_data_bad)
print(f'Task 3 : {response_3_4.text}')