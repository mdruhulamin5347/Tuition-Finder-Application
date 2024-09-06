from django.urls import path
from .views import LOGINPAGE,LOGOUTPAGE,SIGNUP,CHANGE,PasswordReset


urlpatterns = [
    path('login/',LOGINPAGE,name='login'),
    path('logout/',LOGOUTPAGE, name='logout'),
    path('signup/',SIGNUP, name='signup'),
    path('change/',CHANGE, name='change_password'),
    path('password-reset/',PasswordReset, name='password_reset'),  
]
