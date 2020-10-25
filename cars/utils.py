import requests
from .models import Car


def get_external_data(provided_data):
    if "model" and "make" not in provided_data:
        return []
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{}?format=json'.format(
        provided_data["make"])
    cars_in_ext_api = requests.get(url).json()['Results']
    found_item = [
        item for item in cars_in_ext_api if item['Model_Name'] == provided_data["model"]]
    return found_item
