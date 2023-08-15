# scraper/serializers.py
from rest_framework import serializers
from .models import ScrapeResult

class KeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField(max_length=100)
    rows = serializers.IntegerField(min_value=1,max_value=50)

class ScrapeResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScrapeResult
        fields = (
            'custom_id',
            'product_title',
            'image',
            'info',
            'price',
            'user'
        )

        extra_kwargs = {
            'user': {'write_only': True},
            'custom_id': {'write_only': True},
        }