import json
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Car, Rate
from .serializers import CarSerializer, RateSerializer
from .utils import get_external_data
from .exceptions import BadRequest, NotFound


@api_view(['GET', 'POST'])
def cars(request):
    """
    GET: presents all cars in DB
    POST: communicates with external API, checks if car with specific make and model exists;
    if it does, the car is saved in DB, accepted data format: {"make": "kia", "model": "Picanto"}
    """
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    else:
        # insert a new record for a car if exists in external DB
        if not ("make" in request.data and "model" in request.data):
            raise BadRequest()
        item_in_api = get_external_data(request.data)
        if not item_in_api:
            raise NotFound()
        else:
            # saving to db, but if it already exist, will not be created again
            Car.objects.get_or_create(
                make=request.data["make"],
                model=request.data["model"])
        return Response(request.data)


@api_view(['POST'])
def rate(request):
    """
    POST: used to rate cars,
    accepted data format i.e {"make": "fiat", "model": "Strada", "score": 3}
    """
    data = request.data
    if not ("make" in data and "model" in data and "score" in data):
        raise BadRequest()
    car = Car.objects.filter(model=data["model"], make=data["make"])
    if not car:
        raise NotFound('Rate was given to nonexistent car')
    else:
        # queryset acts like a list; this queryset has exactly 1 item if not
        # empty
        car = car[0]

    try:
        Rate.objects.create(model=car, score=data["score"])
        car.update_self(data)
        car.save()
        return Response({"score": data["score"]})
    except ValidationError:
        raise BadRequest("Score out of 1-5 range")


@api_view(['GET'])
def popular(request):
    """
    GET - presents all cars present in database, sorted by popularity - number of rates
    """
    popular_cars = Car.objects.all().order_by("-number_of_rates")
    popular_cars_serializer = CarSerializer(popular_cars, many=True)
    return Response(popular_cars_serializer.data)
