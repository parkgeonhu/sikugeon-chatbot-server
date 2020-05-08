import pytest
from app.models import *
from app.api.views import *
    
@pytest.mark.django_db  
def test_parsing():
    update_data()
    store = Store.objects.get(name="동화가든")
    assert store.shortcode=='B50FQs0HTJI'
    
def test_hashtag_search():
    posts_set=get_post("구파발맛집")
    result=hash_search(posts_set)
    assert result['template']['outputs'][0]['carousel']['items'][0]['title']=='hello_saige'
    
    
    