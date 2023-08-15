# scraper/serializers.py
from rest_framework import serializers

class KeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField(max_length=100)
    rows = serializers.IntegerField(min_value=1,max_value=50)


# scraper/serializers.py
from rest_framework import serializers
from .models import ScrapeResult

class ScrapeResultSerializer(serializers.ModelSerializer):

    custom_id = serializers.CharField(write_only=True)

    class Meta:
        model = ScrapeResult
        fields = (
            'custom_id',
            'product_title',
            'image',
            'info',
            'price',
        )
