# Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from webjudge.forms import SignUpForm
# Vistas
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, redirect
# Otros
from django.http import HttpResponse
import simplejson as json
from webjudge.models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
# end imports


# Renderizar el template de la página home. Principalmente las funciones del frontend.
# Como funciona la autentificacion:
#   Cualquier clase o vista que contenga el aprametro "LoginRequiredMixin" comprobará si nos hemos logeado.
#   Si no lo hemos hecho, nos dirigirá al login y no podremos ver el contenido.

class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template)


class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})

# Función de registro de un usuario nuevo, alumno por defecto.
def signup(request):
    # obtenemos el POST
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # Si el formulario es valido, entonces...
        if form.is_valid():
            # Guardamos el usuario en la tabla de usuarios de django
            user = form.save()
            user.refresh_from_db()  # Recogemos el objeto creado en la tabla
            # Asignamos a variables los valores obtenidos del formulario
            name = form.cleaned_data.get('first_name')
            surname = form.cleaned_data.get('last_name')
            # Creamos nuevo objeto de usuarios de webjudge
            newuser = Users(user=user, role='alumno', name=name, surname=surname)
            newuser.save()
            # Por comodidad al usuario, hacemos login directamente si todo ha salido bien.
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    # Si no es valido, devuelve un formulario vacio, que no crea un usuario y nos hace registrarnos otra vez.
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Vista para la subida de archivos al servidor

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        print(" file saved! ")
    return render(request, 'index.html')



# FUNCIONES DE LA API
# Clase con la que gestionamos que función se debe ejecutar dependiendo del tipo de paso recibido.
class step_functions:

    def saveteststeps(self, test_id, count, argument, description, basestep_id, basestep_name):
        # Creamos un nuevo modelo con test_steps y lo insertamos en la BD.
        newteststeps = Test_steps(
            test_id=test_id,
            step_number=count,
            step_argument=argument,
            step_description=description,
            basestep_id=basestep_id,
            basestep_name=basestep_name
        )
        newteststeps.save()

# Funcion para crear un test. Obtiene una request y crea el test.
@csrf_exempt
def create_test(request):
    # Obtenemos el diccionario que se ha pasado en la peticion.
    test_data = json.loads(request.body)
    # Creamos un nuevo objeto a partir del modelo "Tests", usando como argumentos su campos y el valor que queremos darles.
    newtest = Tests(name=test_data['name'], created_by=test_data['created_by'], test_description=test_data['test_description'], test_tries=0)
    # Guardamos el modelo en la BD.
    newtest.save()
    # Devolvemos un OK.
    return HttpResponse("200")

# Funcion que dada una ID de un test y unos pasos, los crea en la base de datos.
@csrf_exempt
def create_test_steps(request):
    # Obtenemos el diccionario que se ha pasado en la peticion.
    test_steps = json.loads(request.body)
    # Guardamos en test_id en una variable mas accesible
    test_id = test_steps['test_id']
    # Creamos el objeto que contiene la creación de los pasos de los tests, y empezamos un count
    step_funcs = step_functions()
    count = 0
    # Iteramos sobre el diccionario. Por cada paso que hay, lo guardamos en la bd.
    for step in test_steps["steps"]:
        count = count + 1
        step_funcs.saveteststeps(test_id, count, step['argument'], step['description'], step['basestep_id'], step['basestep_name'])

    return HttpResponse("200")

# @csrf_exempt
# def execute_test(request):



