from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
app_name = 'managementApps'

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('home/',views.home,name='home'),
    path('home/site/',views.site,name="site"),
    path('home/partner/',views.partner,name="partner")
]