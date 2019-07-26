
from django.contrib import admin
from django.urls import path

from weather.views import home, delete_city

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('delete/<city_name>/', delete_city, name = 'delete'),
]
