from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('fixuSystem/admin/', admin.site.urls, name="admin"),

    # URLs de home_page y menus
    path('fixuSystem/', include('home_page.urls')),

    # URLs de gestion_login
    path('fixuSystem/access/', include('gestion_login.urls')),

    # URLs de gestion_pacientes
    path('fixuSystem/pacientes/', include('gestion_pacientes.urls')),

    # URLs de gestion_citas
    path('fixuSystem/citas/', include('gestion_citas.urls')),

    # URLs de gestion_consultas
    path('fixuSystem/consultas/', include('gestion_consultas.urls')),

    # URLs de gestion_clinca
    path('fixuSystem/clinica/', include('gestion_clinica.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
