from django.shortcuts import render
from django.http import HttpResponse
from .models import Status
from .make_json import load_json, make_json
from operator import eq
# Create your views here.

def get_status(request):
    _live_members = Status.objects.filter(in_salon=True)
    live_members = []
    for i in range(_live_members.count()):
        live_members.append(_live_members[i].get_name())
    return render(request, 'status.html',
                  {'live_members': live_members})

def post_status(request):
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
            s_name = parsed_data["name"]
            update = parsed_data["update"]
            if eq(update,"entered"):
                b_is_salon = True
            else:
                b_is_salon = False
            new_status = Status(name=s_name,
                                        in_salon=b_is_salon)
            new_status.save()
        except Exception:
            print('{"result" : "fail", "message" : "DB error"}')
            return HttpResponse('{"result" : "fail", "message" : "DB error"}',
                                content_type='application/json; charset=utf-8')
        return HttpResponse('{"result" : "success"}',
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST error"}',
                            content_type='application/json; charset=utf-8')
