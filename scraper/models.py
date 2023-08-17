# scraper/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScrapeResult(models.Model):

    custom_id = models.CharField(max_length=500, unique=True)
    product_title = models.CharField(max_length=200)
    image = models.URLField(null=True,blank=True)
    info = models.TextField(null=True,blank=True)
    price = models.CharField(max_length=50,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.custom_id = f"{self.product_title}_{self.price}_{self.image}_{self.user.id}"
        super(ScrapeResult, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_title