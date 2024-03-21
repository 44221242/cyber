import urllib.request
import json

def get_ip_address():
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        flag = data['country_code']
        ip = data['IPv4']
        city = data['city']
        latitude = data['latitude']
        longitude = data['longitude']

    return flag, ip, city, latitude, longitude
