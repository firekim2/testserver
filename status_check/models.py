from django.db import models
from .make_json import load_json
# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=50, blank=True, default='noname')
    in_salon = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def json_coordinate(self):
        return {'name': self.name}
