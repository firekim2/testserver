from django.shortcuts import render
from django.http import HttpResponse
from .models import Coordinate
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from .make_json import load_json, make_json
import urllib
# Create your views here.

def get_coordinate(request):
    _coordinates = Coordinate.objects.filter(validation=True)
    coordinates = []
    for i in range(_coordinates.count()):
        coordinates.append(_coordinates[i].json_coordinate())
    result = {"coordinates": coordinates}
    result = make_json(result)
    return HttpResponse(result, content_type='application/json; charset=utf-8')

def near_coordinate(request):
    if request.method == 'POST':
        request_data = request.body.decode('utf-8')
        request_data = request_data.replace('status=', '')
        try:
            parsed_data = load_json(request_data)
        except Exception:
            print('{"result" : "fail", "message" : "parsing error"}')
            return HttpResponse('{"result" : "fail", "message" : "parsing error"}',
                                content_type='application/json; charset=utf-8')
        try:
            f_latitude = float(parsed_data["latitude"])
            f_longtitude = float(parsed_data["longtitude"])
            user_location = Point(f_longtitude, f_latitude)
        except Exception:
            print('{"result" : "fail", "message" : "DB error"}')
            return HttpResponse('{"result" : "fail", "message" : "DB error"}',
                                content_type='application/json; charset=utf-8')
        _coordinates = Coordinate.objects.filter(geometry__distance_lte=(user_location, D(km=1)))
        coordinates = []
        for i in range(_coordinates.count()):
            coordinates.append(_coordinates[i].json_coordinate())
        result = {"coordinates": coordinates}
        print(result)
        result = make_json(result)
        return HttpResponse(result, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST error"}',
                            content_type='application/json; charset=utf-8')

def post_coordinate(request):
    if request.method == 'POST':
        request_data = request.body.decode('utf-8')
        request_data = request_data.replace('status=', '')
        print(request)
        try:
            parsed_data = load_json(request_data)
        except Exception:
            print('{"result" : "fail", "message" : "parsing error"}')
            return HttpResponse('{"result" : "fail", "message" : "parsing error"}',
                                content_type='application/json; charset=utf-8')
        try:
            s_name = parsed_data["name"]
            f_latitude = float(parsed_data["latitude"])
            f_longtitude = float(parsed_data["longtitude"])
            f_rotation = float(parsed_data["rotation"])
            point = Point(f_longtitude, f_latitude)
            new_coordinate = Coordinate(name=s_name,
                                        rotation=f_rotation,
                                        geometry=point)
            print(new_coordinate.json_coordinate())
            new_coordinate.save()
        except Exception as inst:
            print(inst)
            print('{"result" : "fail", "message" : "DB error"}')
            return HttpResponse('{"result" : "fail", "message" : "DB error"}',
                                content_type='application/json; charset=utf-8')
        return HttpResponse('{"result" : "success"}',
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST error"}',
                            content_type='application/json; charset=utf-8')
