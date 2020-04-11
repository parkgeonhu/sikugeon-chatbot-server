import requests
import json
import os
##input_place=input('입력하실 태그? ')


#키워드 장소 검색 (ex. 정통집 건대)
def get_store_info(query):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query='+query
    headers = {'Authorization':'KakaoAK '+os.environ['kakaotoken']}
    response = requests.get(url, headers = headers)
    info = json.loads(response.text)
    return info

#지역 검색 (ex. 하계동) 
def get_location_info(query):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+query
    headers = {'Authorization':'KakaoAK '+os.environ['kakaotoken']}
    response = requests.get(url, headers = headers)
    info = json.loads(response.text)
    print(query+' '+str(info))
    return info

class InfoEntity:
    def __init__(self, info):
        self.info = info
        
    def get_name(self):
        return self.info["documents"][0]['place_name']
    
    def get_address(self):
        return self.info["documents"][0]['road_address_name']
    
    def get_x(self):
        return self.info["documents"][0]['x']

    def get_y(self):
        return self.info["documents"][0]['y']
    
    def get_url(self):
        return self.info["documents"][0]['place_url']


# def get_location_name(info):
#     return info["documents"][0]['place_name']

# def get_location_address(info):
#     return info["documents"][0]['road_address_name']

# def get_location_x(info):
#     return info["documents"][0]['x']

# def get_location_y(info):
#     return info["documents"][0]['y']

# def get_location_url(info):
#     return info["documents"][0]['place_url']

# def get_location_category_group_name(info):
#     pass

# if __name__ == '__main__':
#     info={
#         "documents" : [
#             {
#                 "place_name" : "hello",
#                 "x" : 3,
#                 "y" : 3,
#             }
#         ]
#     }
#     entity=InfoEntity(info)
#     print(entity.get_name())
    

    