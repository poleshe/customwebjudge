from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# Este archivo sirve para crear nuevos formularios a partir de modelos (tablas de la BD).
# Se crea un objeto con cada una de las rows de la tabla, y algunas extras si queremos, que podemos colocar en un template directamente
# Al usar la funcion save en uno de estos formularios guardaremos en la BD una nueva linea con los datos del formulario.

# Formulario SignUpForm
class SignUpForm(UserCreationForm):
    # campos extras y información extra para el form. Salen en forma de ayuda.
    username = forms.CharField(max_length=30, help_text='El usuario con el que accederás a la web. Solo letras, numeros y @/./+/-/_.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Tu nombre. Será visible en la web.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Tu apellido. Será visible en la web.')
    email = forms.EmailField(max_length=254, help_text='Obligatorio. Por favor, introduce un email válido.')
    # Campo meta, le decimos el nombre del modelo y el orden de los campos.
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    # Funcion init para añadir a cada campo del formulario la clase "form-control" de bootstrap que les da un estilo muy bonito.
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NewTestForm(forms.ModelForm):

    name = forms.CharField(max_length=30, required=False, help_text='El nombre del Test.')
    created_by = forms.CharField(max_length=30, required=False, help_text='Creado por... Puedes usar tu nombre o el de tu organización.')
    test_description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}),max_length=255, required=False, help_text='Explicación del test. Deberia contener una introduccion, una breve explicacion, y un par de ejemplos de entrada / salida.')
    class Meta:
        model = Tests
        fields = ('name', 'created_by', 'test_description')