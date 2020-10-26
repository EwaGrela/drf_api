import requests
from .models import Car


def get_external_data(provided_data):
    if "model" and "make" not in provided_data:
        print("not provided")
        # return []
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{}?format=json'.format(
        provided_data["make"])
    cars_in_ext_api = requests.get(url).json()['Results']
    found_item = [
        item for item in cars_in_ext_api if item['Model_Name'] == provided_data["model"]]
    return found_item


def validate_car_data(data):
    if not ("make" in data and "model" in data):
        return False
    if not (isinstance(data["make"], str) and isinstance(data["model"], str)):
        return False
    return True


def validate_score_data(data):
    if not ("make" in data and "model" in data and "score" in data):
        return False
    if not (isinstance(data["make"], str) and isinstance(data["model"], str)):
        return False
    if not isinstance(data["score"], int):
        return False
    return True
