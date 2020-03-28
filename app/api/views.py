#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .parser import get_sikugeon_list


# Create your views here.
@csrf_exempt
def dataParsing(request):
    print(request.body.decode('utf-8'))
    
    # response=json.loads(request.body)
    
    places=get_sikugeon_list()
    
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
