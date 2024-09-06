from django.urls import path
from .views import CONTACT
urlpatterns = [
    path('contact/', CONTACT.as_view(), name='contact'),
]
