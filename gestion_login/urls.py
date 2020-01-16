from django.urls import path
from .views import user_login_view, user_logout_view



urlpatterns = [

#########################################
#                                       #
#        URLS DE GESTION_LOGIN          #
#                                       #
#########################################

    path('login/', user_login_view.as_view(), name = 'user-login'),
    path('logout/', user_logout_view.as_view(), name = 'user-logout'),
]
