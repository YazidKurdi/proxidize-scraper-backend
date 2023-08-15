from django.urls import path

from .views import ProductScrapeView, UserScrapeResultListView

urlpatterns = [
    path('scrape/', ProductScrapeView.as_view()),
    path('user/scrape-results/', UserScrapeResultListView.as_view())
]
