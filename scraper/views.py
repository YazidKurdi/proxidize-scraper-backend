from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from scraper import StandardResultsSetPagination
from .models import ScrapeResult
from .serializers import KeywordSerializer,ScrapeResultSerializer
from .scraper import EcommerceScraper


class ProductScrapeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = KeywordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        keyword = serializer.validated_data['keyword']
        rows = serializer.validated_data['rows']

        # Create an instance of the EcommerceScraper class
        scraper = EcommerceScraper()

        # Call the scrape_website method of the EcommerceScraper instance
        scraped_data = scraper.scrape_website(self.request,keyword,rows)

        return Response(scraped_data, status=status.HTTP_200_OK)

class UserScrapeResultListView(ListAPIView):

    serializer_class = ScrapeResultSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['product_title']  # Specify fields to search

    def get_queryset(self):
        user = self.request.user
        queryset = ScrapeResult.objects.filter(user=user)
        return queryset
