from django.urls import path
from .views import HomeView, ResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('results/', ResultsView.as_view(), name='search_results'),
]
