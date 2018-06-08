from django.test import TestCase

# Create your tests here.
from .models import Coordinate
import requests
local_url = 'http://localhost:8000/girlstatue/post_coordination'
#server_url = 'http://alpha.innocean.com/techbook/content/upload/'


def request_test():
    raw = 'status={"name": "nameabc", "latitude": "14.114908174", "longtitude": "178.1039481234", "rotation": "123.141414156"}'
    r = requests.post(local_url, data=raw)
