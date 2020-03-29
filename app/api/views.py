#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .parser import get_sikugeon_list
from .kakaomap import *
from app.models import Store


#비동기 처리를 위해서
def serviceWorker(places):
    for place in places:
        if len(Store.objects.filter(name=place)) > 0:
            break
        info=get_store_info(place)
        loc_x=get_location_x(info)
        loc_y=get_location_y(info)
        Store.objects.create(name=place, loc_x=loc_x ,loc_y=loc_y)
        
# Create your views here.
@csrf_exempt
def dataParsing(request):
    print(request.body.decode('utf-8'))
    
    # response=json.loads(request.body)
    
    places=get_sikugeon_list()
    
    serviceWorker(places)
    
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "파싱 완료"
                    }
                }
            ]
        }
    }

    return JsonResponse(result, status=200)

@csrf_exempt
def reply(request):
    print(request.body.decode('utf-8'))
    
    response=json.loads(request.body)
    
    location=response["action"]["params"]["location"]
    
    
    
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": location
                    }
                }
            ]
        }
    }


    return JsonResponse(result, status=200)
