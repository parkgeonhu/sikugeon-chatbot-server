#-*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def reply(request):
    print(request.body.decode('utf-8'))
    result = {"test": "No order received"}
    return JsonResponse(result, status=200)
    