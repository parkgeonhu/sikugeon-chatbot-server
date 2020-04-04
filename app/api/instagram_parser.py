import requests
import json
import sys
import os

def get_next_page(query_hash, user_id, has_next_page, end_cursor, payload):
    if has_next_page is False:
        return
    else:
        next_url = 'https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+user_id+'","first":12,"after":"'+end_cursor+'"}'
        req = requests.get(next_url)
        temp = json.loads(req.text)
        timeline=temp['data']['user']['edge_owner_to_timeline_media']['edges']
        for post in timeline:
            text=post['node']['edge_media_to_caption']['edges'][0]['node']['text']
            pic_url=post['node']['display_url']
            tags=''
            idx=text.find('#식후건')
            if idx != -1:
                tags=text[idx:]
                data={
                    'pic_url' : pic_url,
                    'tags' : tags
                }
                payload.append(data)

        _has_next_page = temp['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        _end_cursor = temp['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        get_next_page(query_hash, user_id, _has_next_page, _end_cursor, payload)
        
        


## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_payload():
    
    req=requests.get('https://www.instagram.com/sikugeon/?__a=1')

    payload=[]

    profile = json.loads(req.text)


    for post in profile['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        text=post['node']['edge_media_to_caption']['edges'][0]['node']['text']
        pic_url=post['node']['display_url']
    
        tags=''
        idx=text.find('#식후건')

        if idx != -1:
            tags=text[idx:]
            data={
                'pic_url' : pic_url,
                'tags' : tags
            }
            payload.append(data)


    print(profile['graphql']['user']['id'])

    user_id=profile['graphql']['user']['id']
    end_cursor=profile['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    has_next_page=profile['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

    query_hash='d496eb541e5c789274548bf473cc553e'
    
    next_url='https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+user_id+'","first":12,"after":"'+end_cursor+'"}'

    get_next_page(query_hash, user_id, has_next_page, end_cursor, payload)

    print(len(payload))

    # with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as f:
    #     f.write(str(payload))
    # #[{'pic_url':' ','tag':' '},,,]
    return payload


def get_stores(posts: list):
    stores=[]
    for post in posts:
        tags=post['tags'].split(' ')
        # #식후건_남영동_모범식당 #식후건_메모_example
        place=tags[0].split('_')
        query=place[1]+' '+place[2]
        pic_url=post['pic_url']
        data={
            'query' : query,
            'pic_url' : pic_url
        }
        stores.append(data)
        
    return stores