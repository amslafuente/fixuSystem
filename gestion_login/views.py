########## Views de gestion_login ##########

from django.shortcuts import render, reverse
from django.http import request, HttpResponseRedirect
from django.contrib import messages
from .forms import user_login_form
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

########## LOGIN USUARIO VIEW ##########
# View para mostrar el login de usuario
# Usa el template user_login_tpl

class user_login_view(View):

    def post(self, request):

        ctx = dict()
        # Pasa la form completada al contexto
        form = user_login_form(request.POST)
        ctx['form'] = form
        # Recuepera URL next
        ctx['next'] = request.POST['next']

        # La form SI es validada autentifica al usuario
        if form.is_valid():
            # Comprueba que existe
            user = authenticate(username = request.POST['username'], password = request.POST['password'])
            if user is not None:
                # Loge al usuario
                login(request, user)
                # Redirige al punto del que vino
                return HttpResponseRedirect(ctx['next'])
            else:
                # SI no existe ese usuario
                messages.warning(request, 'Ningún/a usuario/a con esos datos')
                return render(request, 'user_login_tpl.html', ctx)
        else:
        # La Form NO es validada manda mensaje de error
            messages.warning(request, 'Errores en el formulario')
            return render(request, 'user_login_tpl.html', ctx)

    def get(self, request):

        ctx = dict()
        # Pasa la form vacia al conexto
        form = user_login_form()
        ctx['form'] = form
        # Pasa URL next al contexto del  template para recuperarlo en post
        ctx['next'] = request.GET['next']
        # Renderiza el form
        return render(request, 'user_login_tpl.html', ctx)

########## LOGOUT USUARIO VIEW ##########
# View para mostrar el logout de usuario
# Usa el template user_logout_tpl

class user_logout_view(View):

    def post(self, request):

        ctx = dict()
        # Desconecta el usuario y reenvia al principio
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('home-page'))

    def get(self, request):

        ctx = dict()
        # Renderiza el form
        return render(request, 'user_logout_tpl.html', ctx)
