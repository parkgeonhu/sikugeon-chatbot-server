from django.db import models


class StoreManager(models.Manager):
    def create_store(self, name, street_address, shortcode, pic_url, place_url, memo, loc_x ,loc_y):
        store = self.create(name=name, street_address=street_address, pic_url = pic_url, place_url=place_url ,memo=memo ,loc_x=loc_x ,loc_y=loc_y, shortcode=shortcode)
        store.create_review_url()
        # do something with the book

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=64, help_text='가게 이름')
    street_address = models.CharField(max_length=128, blank=True, help_text='도로명 주소(신 주소)')
    place_url = models.URLField(max_length = 200, blank=True)
    pic_url = models.URLField(max_length = 200, blank=True)
    review_url = models.URLField(max_length = 200, blank=True)
    shortcode = models.CharField(max_length=64, blank=True, help_text='가게를 구별할 수 있는 unique 코드, instagram/p/{shortcode}')
    loc_x = models.FloatField(null=True)
    loc_y = models.FloatField(null=True)
    memo = models.TextField(help_text='식후건 리뷰', blank=True)
    
    objects = StoreManager()
    
    
    def create_review_url(self):
        self.review_url='https://instagram.com/p/'+self.shortcode
        print(self.review_url)
        self.save()
        
    
    def __str__(self):
        return self.name