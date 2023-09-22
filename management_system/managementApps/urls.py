from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
app_name = 'managementApps'

urlpatterns = [
  
    path('login/', views.custom_login, name='custom_login'),
    
    path('home', views.site, name='create_site'),
    path('home/site', views.site, name="create_site"),
    path('home/site/update/<int:site_id>',views.update_site,name='update_site'),
    path('home/partner', views.partner, name="create_partner"),

    path('home/add-site',views.add_site,name="add_site"),
    path('home/add-partner',views.add_partner,name="add_partner"),
    path('home/partner/update/<int:partner_id>',views.update_partner,name='update_partner'),

    path('add_user/', views.add_user, name='add_user'),
    path('user_list', views.user_list, name='user_list'),
    path('update_user/<int:id>',views.update_user,name='update_user'),
    path('logout/', views.logout_view, name='logout'),
   
 
]