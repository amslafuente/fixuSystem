########## Forms de gestion_login ##########

from django import forms
from django.conf import settings

###############################################################################

# Form para login

class user_login_form(forms.Form):

    # Campos del formulario
    username = forms.CharField(label = 'Usuario/a:', max_length = 150, required = True)
    password = forms.CharField(label = 'Password:', max_length = 150, required = True, widget = forms.PasswordInput)

    ###############################################################################
