import requests
from settings import GOOGLE_MAP_KEY

def get_location(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (address, GOOGLE_MAP_KEY)
    response = requests.get(url)
    return response.json()