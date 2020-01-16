from django.shortcuts import render, reverse
from django.http import request, HttpResponseRedirect
from django.contrib import messages
from .forms import user_login_form
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse



#########################################
#                                       #
#           LOGIN DE USUARIO/A          #
#                                       #
#########################################

class user_login_view(View):

    def post(self, request):

        ctx = dict()
        form = user_login_form(request.POST)
        ctx['form'] = form
        # Recupera URL next
        ctx['next'] = request.POST['next']

        if form.is_valid():
            # Comprueba que existe
            user = authenticate(username = request.POST['username'], password = request.POST['password'])
            if user is not None:
                # Loge al usuario
                login(request, user)
                # Redirige al punto del que vino
                return HttpResponseRedirect(ctx['next'])
            else:
                # Si no existe ese usuario
                messages.warning(request, 'Ningún/a usuario/a con esos datos')            
                return render(request, 'user_login_tpl.html', ctx)
        else:
            messages.warning(request, 'Errores en el formulario')        
            return render(request, 'user_login_tpl.html', ctx)

    def get(self, request):

        ctx = dict()
        form = user_login_form()
        ctx['form'] = form
        # Pasa URL next al contexto del  template para recuperarlo en post
        ctx['next'] = request.GET['next']
        return render(request, 'user_login_tpl.html', ctx)



#########################################
#                                       #
#          LOGOUT DE USUARIO/A          #
#                                       #
#########################################

class user_logout_view(View):

    def post(self, request):

        ctx = dict()
        # Desconecta el usuario y reenvia al principio
        if request.user.is_authenticated:
            logout(request)        
        return HttpResponseRedirect(reverse('home-page'))

    def get(self, request):

        ctx = dict()        
        return render(request, 'user_logout_tpl.html', ctx)
