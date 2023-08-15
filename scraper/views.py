# scraper/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import KeywordSerializer
from .scraper import scrape_website


class ProductScrapeView(APIView):
    def post(self, request, format=None):
        serializer = KeywordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        keyword = serializer.validated_data['keyword']
        scraped_data = scrape_website(keyword)
        return Response(scraped_data, status=status.HTTP_200_OK)
