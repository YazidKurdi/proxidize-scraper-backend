from django.urls import path

from .views import ProductScrapeView

urlpatterns = [
    path('scrape/', ProductScrapeView.as_view()),
]
