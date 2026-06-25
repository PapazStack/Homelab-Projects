import requests, json, datetime

services = {'n8n': '',
    'grafana': '',
    'plex': ''}

discord_webhook = ''

service_status = {}

try:
    with open('last_known.json', 'r') as file:
        last_known = json.load(file)
except:
    last_known = {}

        

for service, url in services.items():
    try:
        health = requests.get(url, timeout=5)
        if health.status_code == 200:
            print(service.title() + ': Healthy')
            service_status[service] = 'Healthy'
        else:
            print(service.title() + ': Unhealthy')
            service_status[service] = 'Unhealthy'
    except:
        print(service.title() + ': Unreachable')
        service_status[service] = 'Unreachable'

for service, status in service_status.items():
    if status != last_known.get(service, 'Healthy'):
        print('Status has changed to ' + status)
        requests.post(discord_webhook, json={'content': service.title() + ' status has changed to ' + status + '.'})
        with open('last_known.json', 'w') as file:
            service_logs = {'Service': service.title(), 'Status': status, 'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')}
            json.dump(service_status, file)   
    if status == 'Unhealthy' or status == 'Unreachable':
        print()
        with open('homelab_log.json', 'a') as file:
            service_logs = {'Service': service.title(), 'Status': status, 'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')}
            json.dump(service_logs, file)
            file.write('\n')    


    

