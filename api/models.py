from django.db import models


class City(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    lat = models.FloatField(verbose_name='Широта в градусах')
    lon = models.FloatField(verbose_name='Долгота в градусах')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
