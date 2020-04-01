from django.db import models


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=64, help_text='가게 이름')
    street_address = models.CharField(max_length=128, blank=True, help_text='도로명 주소(신 주소)')
    place_url = models.URLField(max_length = 200, blank=True)
    loc_x = models.FloatField(blank=True)
    loc_y = models.FloatField(blank=True)
    memo = models.TextField(help_text='식후건 리뷰', blank=True)
    
    def __str__(self):
        return self.name