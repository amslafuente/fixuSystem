"""fixuSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('fixusystem/admin/', admin.site.urls, name="admin"),

    # URLs de home_page y menus
    path('fixusystem/', include('home_page.urls')),

    # URLs de gestion_login
    path('fixusystem/access/', include('gestion_login.urls')),

    # URLs de gestion_pacientes
    path('fixusystem/pacientes/', include('gestion_pacientes.urls')),

    # URLs de gestion_citas
    path('fixusystem/citas/', include('gestion_citas.urls')),

    # URLs de gestion_consultas
    path('fixusystem/consultas/', include('gestion_consultas.urls')),

    # URLs de gestion_clinca
    path('fixusystem/clinica/', include('gestion_clinica.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
