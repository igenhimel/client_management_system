from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
app_name = 'managementApps'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.site, name='create_site'),
    path('home/site', views.site, name="create_site"),
    path('home/partner', views.partner, name="create_partner"),
    path('home/site/update/<int:site_id>',views.update_site,name='update_site'),
    path('home/partner/update/<int:partner_id>',views.update_partner,name='update_partner'),


]
