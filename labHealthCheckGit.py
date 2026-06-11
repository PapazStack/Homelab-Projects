import requests

services = {'n8n': 'https://homelabURL.here',
    'grafana': 'https://homelabURL.here',
    'plex': 'https://homelabURL.here'}

for service, url in services.items():
    try:
        health = requests.get(url)
        if health.status_code == 200:
            print(service.title() + ': Healthy')
        else:
            print(service.title() + ' Unhealthy')
    except:
        print(service.title() + ' Unreachable')