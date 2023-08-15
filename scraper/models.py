# scraper/models.py
from django.db import models

class ScrapeResult(models.Model):

    custom_id = models.CharField(max_length=255, unique=True)
    product_title = models.CharField(max_length=200)
    image = models.URLField()
    info = models.TextField()
    price = models.CharField(max_length=50)


    def save(self, *args, **kwargs):
        self.custom_id = f"{self.product_title}_{self.price}_{self.image}"
        super(ScrapeResult, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_title