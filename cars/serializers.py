from rest_framework import serializers
from .models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'make',
            'model',
            'average_rate',
            'sum_rates',
            'number_of_rates')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('model', 'score')
