from .make_json import load_json
from django.contrib.gis.db import models
# Create your models here.


class Coordinate(models.Model):
    validation = models.BooleanField(default=True)
    name = models.CharField(max_length=50, blank=True, default='noname')
    rotation = models.FloatField(blank=False)
    geometry = models.PointField(srid=4326,default='SRID=3857;POINT(0.0 0.0)')
    def __str__(self):
        return self.name

    def json_coordinate(self):
        return {'name': self.name,
                'latitude': str(self.geometry[1]),
                'longtitude': str(self.geometry[0]),
                'rotation': str(self.rotation)}
