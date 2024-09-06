from django.urls import path
from .views import CREATE_PROFILE,PROFILE_VIEW,TUITIONBD ,OTHERPROFILE
from .pdf import profile_pdf
urlpatterns = [
    path('create/',CREATE_PROFILE,name='create'),
    path('view/',PROFILE_VIEW, name='view'),
    path('tuitionbd/',TUITIONBD, name='tuitionbd'),
    path('otherprofile/<int:id>/',OTHERPROFILE,name='otherprofile'),
    path('profile-download-pdf/<int:id>/',profile_pdf, name='pdf'),
]
