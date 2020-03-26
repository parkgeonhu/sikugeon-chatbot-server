#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

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
