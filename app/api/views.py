#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .parser import get_sikugeon_list
from .kakaomap import *
from .image_parser import *
from .instagram_parser import *
from app.models import Store
from haversine import haversine


# #비동기 처리를 위해서
# def serviceWorker(stores):
#     local_store=[]
    
#     # db에 있는 Store 데이터
#     for store in Store.objects.all():
#         local_store.append(store.name)
    
#     create_list_idx=[]
#     for idx, store in enumerate(stores):
#         # local store에 store.name이 없는 경우
#         if store['name'] not in local_store:
#             create_list_idx.append(idx)
#             name=store['name']
#             address=store['address']
#             query=address[address.find('(')+1:address.find(')')]+name
#             memo=store['memo']
            
#             #네이버 이미지 검색 파싱
#             pic_url = get_image_url(query=name)
            
            
#             #카카오맵 파싱
#             info=get_store_info(query)
#             place_url=get_location_url(info)
#             loc_x=get_location_x(info)
#             loc_y=get_location_y(info)
#             Store.objects.create(name=name, street_address=address, pic_url = pic_url, place_url=place_url ,memo=memo ,loc_x=loc_x ,loc_y=loc_y)
        
#         # local store에 store.name이 있으면 local store에서 그 요소를 삭제
#         else:
#             del_index=local_store.index(store['name'])
#             del local_store[del_index]
    
#     #식후건 리스트에서 삭제된 가게 삭제
#     for store in local_store:
#         Store.objects.filter(name=store).delete()
        
        
        
    
#     # origin => 식후건 리스트에 저장된 맛집
#     # local => 현재 django db에 저장되어 있는 맛집
#     local_set=set(local_store)
#     origin_set=set(stores)
    
#     # create_list=list(origin_set-local_set)
#     # delete_list=list(local_set-origin_set)
    
#     #store에 신규 가게 추가
#     for store in create_list:
#         info=get_store_info(store)
#         loc_x=get_location_x(info)
#         loc_y=get_location_y(info)
#         Store.objects.create(name=store, loc_x=loc_x ,loc_y=loc_y)
    
#     #식후건 리스트에서 삭제된 가게 삭제
#     for store in delete_list:
#         Store.objects.filter(name=store).delete()


def update_data():
    payload=get_payload()
    stores=get_stores(payload)
                #카카오맵 파싱
    #기존에 저장되어 있던 store shortcode 불러오기
    local_shortcodes=[]
    
    for store in Store.objects.all():

        local_shortcodes.append(store.shortcode)
        
    
    for store in stores:
        memo=''
        query=store['query']
        pic_url=store['pic_url']
        shortcode=store['shortcode']
        
        if shortcode in local_shortcodes:
            #origin store의 shortcode
            del_index=local_shortcodes.index(shortcode)
            del local_shortcodes[del_index]
            continue
        
        info=get_store_info(query)
        name=get_location_name(info)
        street_address=get_location_address(info)
        place_url=get_location_url(info)
        loc_x=get_location_x(info)
        loc_y=get_location_y(info)
        Store.objects.create_store(name=name, street_address=street_address, pic_url = pic_url, place_url=place_url ,memo=memo ,loc_x=loc_x ,loc_y=loc_y, shortcode=shortcode)
        
        
    #origin list와 local list 비교해서, local list에 남아있는 것은 삭제
    for shortcode in local_shortcodes:
        Store.objects.filter(shortcode=shortcode).delete()    
            
            

@csrf_exempt
def dataParsing(request):
    print(request.body.decode('utf-8'))
    
    # response=json.loads(request.body)

    
    
    update_data()
    
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
    
    # location=response["action"]["params"]["location"]
    
    #user request 원문 그대로 사용 // 추후에 지역만 걸러주는 것을 생각해보자
    location=response['userRequest']['utterance']
    info=get_store_info(location)
    user_x=get_location_x(info)
    user_y=get_location_y(info)
    
    user=(float(user_y), float(user_x))
    stores=Store.objects.all()
    near_store = [store for store in stores
                 if haversine(user, (store.loc_y, store.loc_x)) <= 3]
    
    sikugeon=[]
    for store in near_store:
        if len(sikugeon)>10:
            break
        temp={
           "title": store.name,
           "description":"식후건 메모",
           "thumbnail":{
              "imageUrl":store.pic_url
           },
           "buttons":[
            {
             "action":"webLink",
             "label":"식후건 인스타 리뷰 보기",
             "webLinkUrl": store.review_url
            },
            {
             "action":"webLink",
             "label":"카카오맵으로 연결",
             "webLinkUrl": store.place_url
            }
           ]
        }
        sikugeon.append(temp)
    
    
    result=''

    #맛집이 근처에 없다면
    if len(near_store) == 0:
           result = {
               "version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "simpleText": {
                               "text": "근처에 맛집이 없네요 ㅠㅠ"
                           }
                       }
                   ]
               }
           }
            
    #있으면 데이터 넣어주기
    else :
        result = {'version': '2.0',
            'template': {'outputs': [{'carousel': {'type': 'basicCard',
            'items': sikugeon}}]}}

    return JsonResponse(result, status=200)
