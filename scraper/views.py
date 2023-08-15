from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import KeywordSerializer
from .scraper import EcommerceScraper


class ProductScrapeView(APIView):
    def post(self, request, format=None):
        serializer = KeywordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        keyword = serializer.validated_data['keyword']
        rows = serializer.validated_data['rows']

        # Create an instance of the EcommerceScraper class
        scraper = EcommerceScraper()

        # Call the scrape_website method of the EcommerceScraper instance
        scraped_data = scraper.scrape_website(keyword,rows)

        return Response(scraped_data, status=status.HTTP_200_OK)

