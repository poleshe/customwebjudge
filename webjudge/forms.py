from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='El usuario con el que accederás a la web. Solo letras, numeros y @/./+/-/_.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Tu nombre. Será visible en la web.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Tu apellido. Será visible en la web.')
    email = forms.EmailField(max_length=254, help_text='Obligatorio. Por favor, introduce un email válido.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
