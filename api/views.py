from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import WeatherSerializer
from .yandex_api import get_fact_weather_by_city

CITY = openapi.Parameter(
    'city',
    openapi.IN_QUERY,
    description='Город',
    type=openapi.TYPE_STRING,
    required=False
)


@swagger_auto_schema(manual_parameters=[CITY], methods=['GET'])
@api_view(['GET'])
def get_weather(request: Request):
    """
    Get weather by city name.
    """
    city_name = request.query_params.get('city')
    if not city_name:
        return Response(
            {'error': 'Нет обязательного параметра с названием города'}
        )
    fact_weather = cache.get(city_name.lower())
    if not fact_weather:
        try:
            fact_weather = get_fact_weather_by_city(city_name=city_name)
            cache.set(city_name.lower(), fact_weather)
        except ValueError as err:
            return Response({'error': str(err)})

    serializer = WeatherSerializer(fact_weather)
    return Response(serializer.data)


class GetWeatherView(TemplateView):
    """
    Get weather by city name.
    """
    template_name = 'api/weather.html'

    def get_context_data(self, **kwargs):
        city_name = self.request.GET.get('city').strip()
        if city_name:
            fact_weather = cache.get(city_name)
            if not fact_weather:
                try:
                    fact_weather = get_fact_weather_by_city(city_name=city_name)
                    cache.get(fact_weather)
                except ValueError as err:
                    kwargs.update({'error': str(err)})
                    return super().get_context_data(**kwargs)

            kwargs.update(
                {
                    'city_name': city_name,
                    'obj': fact_weather
                }
            )
        return super().get_context_data(**kwargs)

