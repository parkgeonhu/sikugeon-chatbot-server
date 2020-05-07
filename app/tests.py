import pytest
from app.models import *
from app.api.views import *

# @pytest.mark.django_db
# def test_create_store():
#     Store.objects.create(name="동화가든", shortcode='B50FQs0HTJI')
#     store= Store.objects.get(name="동화가든")
#     assert store.name=='동화가든'

# @pytest.mark.django_db
# def test_store():
#     store = Store.objects.create(name="동화가든", shortcode='B50FQs0HTJI')
#     assert store.name=='동화가든'

    
@pytest.mark.django_db  
def test_parsing():
    update_data()
    store = Store.objects.get(name="동화가든")
    assert store.shortcode=='B50FQs0HTJI'
    
    