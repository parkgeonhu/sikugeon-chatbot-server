import json
import logging as log
import re
import sys
import os
from abc import ABCMeta, abstractmethod
from json import JSONDecodeError

import bs4
import hashlib
import requests

authtokens = tuple()

instagram_root = "https://www.instagram.com"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def checkTokens():
    if not authtokens:
        getTokens()
        
def const_gis(query):
    checkTokens()
    t = authtokens[0] + ':' + query
    x_instagram_gis = hashlib.md5(t.encode("utf-8")).hexdigest()
    return x_instagram_gis

def getTokens():
    r = requests.get('https://instagram.com/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0', }).text
    rhx_gis = json.loads(re.compile('window._sharedData = ({.*?});', re.DOTALL).search(r).group(1))['nonce']

    ppc = re.search(r'ProfilePageContainer.js/(.*?).js', r).group(1)
    r = requests.get('https://www.instagram.com/static/bundles/metro/ProfilePageContainer.js/' + ppc + '.js').text
    query_hash = re.findall(r'{value:!0}\);(?:var|const|let) .=\"([0-9a-f]{32})\"', r)[0]

    global authtokens
    authtokens = tuple((rhx_gis, query_hash))

def useridToUsername(userid):
    checkTokens()
    query_variable = '{"user_id":"' + str(userid) + '","include_reel":true}'
    header = {'X-Instagram-GIS': const_gis(query_variable),
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
              'X-Requested-With': 'XMLHttpRequest'}
    r = requests.get(
        'https://www.instagram.com/graphql/query/?query_hash=' + authtokens[1] + '&variables=' + query_variable,
        headers=header).text
    if json.loads(r).get("message") == 'rate limited':
        print('[x] Rate limit reached!\n[#] Unchecked ID: {}\n[!] Try again in a few minutes..\n'.format(userid))
        exit()
    try:
        username = json.loads(r)['data']['user']['reel']['user']['username']
        return username
    except:
        return False




def extract_shared_data(doc):
    for script_tag in doc.find_all("script"):
        if script_tag.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\._sharedData = ", "", script_tag.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
            return shared_data

def get_query_id(doc):
    query_ids = []
    for script in doc.find_all("script"):
        if script.has_attr("src"):
            text = requests.get("%s%s" % (instagram_root, script['src'])).text
            if "queryId" in text:
                for query_id in re.findall("(?<=queryId:\")[0-9A-Za-z]+", text):
                    query_ids.append(query_id)
    return query_ids

def get_post(tag):
    post_set={}
    url_string = "https://www.instagram.com/explore/tags/%s/" % tag
    response = bs4.BeautifulSoup(requests.get(url_string).text, "html.parser")
    potential_query_ids = get_query_id(response)
    shared_data = extract_shared_data(response)

    media = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']

    for node in media:
        owner_id=node['node']['owner']['id']
        if owner_id not in post_set.keys():
            post_set[owner_id]=[]
        post_set[owner_id].append(node['node'])

    end_cursor = shared_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

    # figure out valid queryId
    success = False
    for potential_id in potential_query_ids:
        variables = {
            'tag_name': tag,
            'first': 4,
            'after': end_cursor
        }
        url = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s" % (potential_id, json.dumps(variables))
        try:
            data = requests.get(url).json()
            if data['status'] == 'fail': #empty response, skip
                continue
            query_id = potential_id
            success = True
            break
        except JSONDecodeError as de: #no valid JSON retured, most likely wrong query_id resulting in 'Oops, an error occurred.'
            pass
    if not success:
        log.error("Error extracting Query Id, exiting")
        sys.exit(1)

    cnt=0
    while end_cursor is not None:
        if cnt==5:
            break
        url = "https://www.instagram.com/graphql/query/?query_hash=%s&tag_name=%s&first=12&after=%s" % (query_id, tag, end_cursor)
        data = json.loads(requests.get(url).text)
        end_cursor = data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        for node in data['data']['hashtag']['edge_hashtag_to_media']['edges']:
            owner_id=node['node']['owner']['id']
            if owner_id not in post_set.keys():
                post_set[owner_id]=[]
            post_set[owner_id].append(node['node'])
        cnt+=1
        print(cnt)
        
    return post_set


# if __name__ == '__main__':
#     extract_recent_tag("구파발맛집")
#     ordering_sequence=[]
#     for key in post_set:
#         ordering_sequence.append((key,len(post_set[key]), useridToUsername(key)))
#     ordering_sequence.sort(key = lambda element : element[1], reverse=True)
    
#     with open(os.path.join(BASE_DIR, 'result.json'), 'w+', encoding='utf8') as f:
#         res=sorted(post_set.items(), key=lambda element : len(element[1]), reverse=True)
#         f.write(str(res))

