from __future__ import absolute_import, unicode_literals
from celery import shared_task
from app.api.tag_search import *
from app.models import *
import json


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

def hash_search(posts_set):
        posts_set_sorted=[]
        for key in posts_set:
            post={
                'userid' : key,
                'count' : len(posts_set[key])
            }
            posts_set_sorted.append(post)
        posts_set_sorted.sort(key = lambda element : element['count'], reverse=True)
        
        items=[]
        cnt=0
        for post in posts_set_sorted:
            if cnt==10:
                break
            post['username']=useridToUsername(post['userid'])
            post['url']="https://instagram.com/"+post['username']

            item={
                "title": post['username'],
               "description":"게시물 개수 : "+str(post['count']),
               "thumbnail":{
                  "imageUrl":post['url']
               },
               "buttons":[
                {
                 "action":"webLink",
                 "label":"인스타 정보 확인하기",
                 "webLinkUrl": post['url']
                }
               ]
            }
            items.append(item)
            cnt+=1
        
        result = {'version': '2.0',
            'template': {'outputs': [{'carousel': {'type': 'basicCard',
            'items': items}}]}}
        return items
        #return result

@shared_task
def hash_task(content, shortcode):
    posts_set=get_post(content)
    result=hash_search(posts_set)
    h=HashTag.objects.get(shortcode=shortcode)
    h.data=json.dumps(result)
    h.save()