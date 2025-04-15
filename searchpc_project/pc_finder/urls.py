from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, ResultsView, SignUpView, CustomLoginView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('results/', ResultsView.as_view(), name='search_results'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
