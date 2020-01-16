from django import forms
from django.conf import settings



#########################################
#                                       #
#             FORMS PARA LOGIN          #
#                                       #
#########################################

class user_login_form(forms.Form):

    username = forms.CharField(label = 'Usuario/a:', max_length = 150, required = True)
    password = forms.CharField(label = 'Password:', max_length = 150, required = True, widget = forms.PasswordInput)
