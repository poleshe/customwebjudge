# Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from webjudge.forms import SignUpForm, NewTestForm
# Vistas
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, redirect
# Otros
from django.http import HttpResponse, JsonResponse
import simplejson as json
from webjudge.models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
import datetime
import os
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

    def post(self, request, *args, **kwargs):
        return render(request, self.template)

class NewTest(LoginRequiredMixin, View):
    template = 'newtest.html'
    login_url = '/login/' 

    def get(self, request):
        form = NewTestForm()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        # create_test(request)
        return HttpResponse(200)

class UploadTest(LoginRequiredMixin, View):
    template = 'uploadtest.html'
    login_url = '/login/' 

    def get(self, request):
        test_id = request.GET['test_id']
        return render(request, self.template,{'test_id': test_id})

    def post(self, request, *args, **kwargs):
        return HttpResponse(200)

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
@csrf_exempt
def upload(request):
    # Si nos llega un post, hacemos...
    if request.method == 'POST':
        # Cogemos el archivo desde request.files
        uploaded_file = request.FILES['document']
        # Cogemos la ID del test, que nos llega por get a través del redirect de create_test
        test_id = request.POST['test_id']
        # Creamos un objecto FileSystemStorage
        fs = FileSystemStorage()
        # Cogemos los datos del test en la db.
        testdb = Tests.objects.get(id=test_id)
        # Creamos un nombre nuevo para el archivo con su id y nombre del test. ID es clave primaria y no puede estar repetido.
        # Además, quitamos la extension .html y la recolocamos al final por si se intenta subir un archivo con una extension que no toca.
        uploaded_file.name = uploaded_file.name.replace('.html','')
        uploaded_file.name = testdb.name + "_" + test_id + ".html"
        uploaded_file.name = uploaded_file.name.replace(' ','')
        # Comprobamos si este archivo ya existe. Si existe, lo borramos y creamos uno nuevo. 
        if os.path.exists("webjudge/testfiles/"+uploaded_file.name):
            print("File exists! Deleting old file...")
            os.remove("webjudge/testfiles/"+uploaded_file.name)
        # Guardamos el archivo en el servidor y soltamos un mensaje de log.
        fs.save(uploaded_file.name, uploaded_file)
        print("Archivo de Test guardado correctamente en "+fs.url(uploaded_file.name))
        # Updateamos la row del test. Añadimos el nombre del archivo y la ruta donde se hará el serve, EJ /media/EjemploTest_4.html
        testdb.test_file_name = uploaded_file.name
        testdb.test_url = fs.url(uploaded_file.name)
        testdb.save()
    # Devolvemos un 200
    return HttpResponse(200)

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
    if request.method == 'POST':
        form = NewTestForm(request.POST)
        if form.is_valid():
            form.save()
            test = Tests.objects.last()
            test_id = test.id
    # Devolvemos un OK junto a un redirect con la ID del test creado por GET.
    return JsonResponse({'redirect': 'true', 'redirect_url':'/uploadtest/?test_id='+str(test_id)+''})
    

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



