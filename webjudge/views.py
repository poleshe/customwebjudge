# Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from webjudge.forms import SignUpForm, NewTestForm
from django.contrib.auth import logout as do_logout
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
import time
# Selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
# end imports


# Renderizar el template de la página home. Principalmente las funciones del frontend.
# Como funciona la autentificacion:
#   Cualquier clase o vista que contenga el aprametro "LoginRequiredMixin" comprobará si nos hemos logeado.
#   Si no lo hemos hecho, nos dirigirá al login y no podremos ver el contenido.

class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/' 
    
    def get(self, request):
        # Obtenemos el objeto de usuario de la BD del usuario actual.
        requestuser = User.objects.get(username=request.user.username)
        # Cogemos sus datos.
        realuser = Users.objects.get(user=requestuser)
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template, {'userinfo':realuser})

    def post(self, request, *args, **kwargs):
        return render(request, self.template)

class NewTest(LoginRequiredMixin, View):
    template = 'newtest.html'
    login_url = '/login/' 

    def get(self, request):
        form = NewTestForm()
        # Obtenemos el objeto de usuario de la BD del usuario actual.
        requestuser = User.objects.get(username=request.user.username)
        # Cogemos sus datos.
        realuser = Users.objects.get(user=requestuser)
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template, {'form': form, 'userinfo':realuser})

    def post(self, request, *args, **kwargs):
        # create_test(request)
        return HttpResponse(200)

class UploadTest(LoginRequiredMixin, View):
    template = 'uploadtest.html'
    login_url = '/login/' 

    def get(self, request):
        test_id = request.GET['test_id']
        # Obtenemos el objeto de usuario de la BD del usuario actual.
        requestuser = User.objects.get(username=request.user.username)
        # Cogemos sus datos.
        realuser = Users.objects.get(user=requestuser)
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template,{'test_id': test_id, 'userinfo':realuser})

    def post(self, request, *args, **kwargs):
        return HttpResponse(200)

class NewSteps(LoginRequiredMixin, View):
    template = 'newsteps.html'
    login_url = '/login/' 

    def get(self, request):
        test_id = request.GET['test_id']
        # Obtenemos el objeto de usuario de la BD del usuario actual.
        requestuser = User.objects.get(username=request.user.username)
        # Cogemos sus datos.
        realuser = Users.objects.get(user=requestuser)
        # Cogemos los datos de los base_steps, que son los esqueletos de los pasos.
        base_steps = Base_steps.objects.all()
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template,{'test_id': test_id, 'userinfo':realuser, 'base_steps': base_steps})

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

# Funcion para cerrar sesion
def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

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
            newuser = Users(user=user, role='Alumno', name=name, surname=surname)
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


# Vista para la subida de archivos al servidor.
@csrf_exempt
def upload(request):
    # Si nos llega un post, hacemos...
    if request.method == 'POST':
        # Comprobamos que archivo es, si el HTML o el JS.
        file_type = request.POST['file_type']
        if(file_type == "html"):
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
            if os.path.exists("webjudge/testfiles/"+test_id+"/"+uploaded_file.name):
                print("File exists! Deleting old file...")
                os.remove("webjudge/testfiles/"+test_id+"/"+uploaded_file.name)
            # Guardamos el archivo en el servidor y soltamos un mensaje de log.
            fs.save(test_id+"/"+uploaded_file.name, uploaded_file)
            print("Archivo de Test guardado correctamente en "+fs.url("/templates/"+test_id+"/"+uploaded_file.name))
            # Updateamos la row del test. Añadimos el nombre del archivo y la ruta donde se hará el serve, EJ /media/EjemploTest_4.html
            testdb.test_file_name = uploaded_file.name
            testdb.test_url = fs.url(test_id+"/"+uploaded_file.name)
            testdb.save()
        else:
            # Cogemos el archivo desde request.files
            uploaded_file = request.FILES['document']
            # Cogemos la ID del test, que nos llega por get a través del redirect de create_test
            test_id = request.POST['test_id']
            # Creamos un objecto FileSystemStorage
            fs = FileSystemStorage()
            # Cogemos los datos del test en la db.
            testdb = Tests.objects.get(id=test_id)
            # Comprobamos si este archivo ya existe. Si existe, lo borramos y creamos uno nuevo. 
            if os.path.exists("webjudge/testfiles/"+test_id+"/"+uploaded_file.name):
                print("File exists! Deleting old file...")
                os.remove("webjudge/testfiles/"+test_id+"/"+uploaded_file.name)
            # Guardamos el archivo en el servidor y soltamos un mensaje de log.
            fs.save(test_id+"/"+uploaded_file.name, uploaded_file)
            print("Archivo de Test guardado correctamente en "+fs.url("/templates/"+test_id+"/"+uploaded_file.name))
            # Updateamos la row del test. Añadimos el nombre del archivo y la ruta donde se hará el serve, EJ /media/EjemploTest_4.html
            testdb.test_answer_name = uploaded_file.name
            testdb.test_answer_url = fs.url(test_id+"/"+uploaded_file.name)
            testdb.save()
    # Devolvemos un 200
    return HttpResponse(200)

# FUNCIONES DE LA API

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
# TODO: EJECUTAR TEST ANTES DE GUARDAR...
@csrf_exempt
def create_test_steps(request):
    
    if request.method == 'POST':
        test_steps = request.POST.get('data', 'default')
        test_steps = json.loads(test_steps)
        steps_count = 1
        for step in test_steps:
            newstep = Test_steps(test_id = step['test_id'], basestep_name = step['basestep_desc'], step_argument = step['step_args'], step_number = steps_count, step_description = "filler")
            newstep.save()
            steps_count = steps_count + 1

        # TODO EXECUTE TEST AND RETURN EITHER TRUE OR FALSE
    return HttpResponse("200")
        
@csrf_exempt
def execute_test(request):
    x = 0




# STEPS CLASS
# Esta clase contiene una funcion por cada paso...

try:
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
except Exception as e:
    print (" Error de coneaxión. ")
    print(e)

class Step_Execution():
    test_id = 0
    global driver
    
    def __init__(self, test_id): 
        self.test_id = test_id
    
    def reloadventana(argument):
        try:
            driver.refresh()
            return True
        except Exception as e:
            print(e)
            print("an error ocurred")

    def clickonid(argument):
        try:
            driver.find_element_by_name(argument).click()
            return True
        except Exception as e:
            print(e)
            print("an error ocurred")
            return False
    
    def esperartexto(argument):
        count=0
        max_tries = 10
        while True:
            if argument in driver.page_source:
                return True
            if count > max_tries:
                print("error happened")
                return False
            else:
                count+=1
                time.sleep(1)

    def escribirenid(argument):
        try:
            input_object = driver.find_element_by_name(argument)
            input_object.send_keys(argument)
            return True
        except Exception as e:
            print(e)
            print("an error ocurred")
            return False

    def wait(argument):
        try:
            driver.implicitly_wait(argument)
            return True
        except Exception as e:
            print(e)
            print("an error ocurred")
            return False

        

    
    


    








































