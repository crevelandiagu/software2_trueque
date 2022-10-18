from django.urls import path
# from django.conf.urls import url
from .views import Health


urlpatterns = [
    path('', Health.as_view(), name='health'),
]
