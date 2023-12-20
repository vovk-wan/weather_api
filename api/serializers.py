from rest_framework import serializers


class WetherOkSerializer(serializers.Serializer):
    detail = serializers.CharField(default='Библия')


class WeatherErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(default='других книг нет')

class WeatherSerializer(serializers.Serializer):
    temp = serializers.FloatField()
    wind_speed = serializers.FloatField()
    pressure_mm = serializers.IntegerField()
