# Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from webjudge.forms import SignUpForm, NewTestForm, ModifyUser
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


#############################################################
##################### CUSTOMWEBJUDGE API ####################
###  En esta api se realizan los render de las templates, ###
###  Se tratan todos los datos que vienen del front       ###
###  Se ejecutan los tests contra el docker de selenium   ###
###  Y se realiza el AUTH de la web, registro, y login.   ###
###  Además, funciona genial :)                           ###
#############################################################


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
        #Cogemos todos los tests para enseñarlos en la lista
        tests = Tests.objects.all()
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template, {'userinfo':realuser, 'tests':tests})

    def post(self, request, *args, **kwargs):
        return render(request, self.template)

class UserAdmin(LoginRequiredMixin, View):
    template = 'user_config.html'
    login_url = '/login/' 
    
    def get(self, request):
        # Obtenemos el objeto de usuario de la BD del usuario actual.
        requestuser = User.objects.get(username=request.user.username)
        # Cogemos sus datos.
        realuser = Users.objects.get(user=requestuser)
        form = ModifyUser(initial={'first_name':realuser.name, 'last_name': realuser.surname, 'email':realuser.user.email})
        # Devolvemos la vista junto a los datos y el nombre del template.
        return render(request, self.template, {'userinfo':realuser, 'form':form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ModifyUser(request.POST)
            # Si el formulario es valido, entonces...
            if form.is_valid():
                # Primero cogemos el usuario que ha pedido el cambio
                user = User.objects.get(username=request.user.username)
                webjudgeuser = Users.objects.get(user=user)
                # Actualizamos nombre, usuario y email
                webjudgeuser.name = form.cleaned_data.get('first_name')
                webjudgeuser.surname = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                # Y guardamos en la base de datos los cambios.
                webjudgeuser.save()
                user.save()
                return redirect('/user_admin/')
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
# Funcion execute_test
# Esta funcion guarda los pasos de un test que ya ha sido validado.
# Tan solo obtiene los pasos y los guarda en la base de datos.
@csrf_exempt
def create_test_steps(request):
    
    if request.method == 'POST':
        test_steps = request.POST.get('data', 'default')
        test_steps = json.loads(test_steps)
        steps_count = 1
        test_id = test_steps[0]['test_id']

        for step in test_steps:
            newstep = Test_steps(test_id = step['test_id'], basestep_name = step['basestep_name'], step_argument = step['step_args'], step_number = steps_count, step_description = "filler")
            newstep.save()
            steps_count = steps_count + 1

        return HttpResponse(status=200)

# Sirve para guardar los pasos en la BD y tambien comprueba si el test es valido.
@csrf_exempt
def create_temporal_test_steps(request):
    # Si es post, manejamos...
    if request.method == 'POST':
        # Obtenemos los datos y los serializamos
        test_steps = request.POST.get('data', 'default')
        test_steps = json.loads(test_steps)
        steps_count = 1
        test_id = test_steps[0]['test_id']
        # Por cada paso, lo guardamos en la base de datos.
        for step in test_steps:
            newstep = Test_steps(test_id = step['test_id'], basestep_name = step['basestep_name'], step_argument = step['step_args'], step_number = steps_count, step_description = "filler")
            newstep.save()
            steps_count = steps_count + 1
        # Comprobamos que funciona usando la funcion test_valido. Dependiendo si es valido o no, enviamos un codigo o otro al frontend.
        valido = test_valido(request, test_id)
    if(valido == True):
        print("El test con id "+str(test_id)+" es valido.")
        return HttpResponse(status=200)
    else:
        print("El test con id "+str(test_id)+" es invalido. Se borraran sus pasos.")
        return HttpResponse(status=500)

    
@csrf_exempt
def execute_test(request):
    # Obtenemos los pasos del test que 
    current_test_steps = Test_steps.objects.filter(test_id=1).order_by("step_number")
    test = Tests.objects.filter(id=1)
    # Obtenemos la url donde esta guardado este test, y la id del test
    test_url = test[0].test_url
    test_id = current_test_steps[0].test_id
    # Creamos un nuevo objeto que ejecuta los steps. Tambien abrimos un nodo de conexion con un navegador chrome.
    step_executer = Step_Execution(test_id)
    step_executer.abrir_nodo()
    # Por cada paso obtenido, lo ejecutamos.
    # TODO SI FALLA .... SI NO FALLA....
    for step in current_test_steps:
        result = getattr(step_executer, step.basestep_name)(step.step_argument)
        print(result)



####################################################################
# Este test se ejecuta cuando queremos crear un test, y comprueba si el test es valido o no, es decir, si se ha completado correctamente.
####################################################################
@csrf_exempt
def test_valido(request, test_id):
    # Obtenemos los pasos del test que se ejecuta y el test
    current_test_steps = Test_steps.objects.filter(test_id=test_id).order_by("step_number")
    test = Tests.objects.filter(id=test_id)
    # Obtenemos la url donde esta guardado este test, y la id del test
    test_url = test[0].test_url
    test_id = current_test_steps[0].test_id
    # Creamos un nuevo objeto que ejecuta los steps. Tambien abrimos un nodo de conexion con un navegador chrome.
    step_executer = Step_Execution(test_id)
    step_executer.abrir_nodo()
    # Por cada paso obtenido, lo ejecutamos.
    # Lo ejecutamos en la clase Step_Execution, en nuestro caso alojada en step_executer. Cada step tiene su propia funcion en la clase.
    # De este modo podemos cambiar los pasos muy facilmente. Si uno de estos pasos falla, se devuelve un False, lo que significa que el test ha fallado.
    # Si no, devuelve un True, y seguimos. Al final borramos los pasos de la base de datos porque no son los pasos finales que queremos usar.
    for step in current_test_steps:
        result = getattr(step_executer, step.basestep_name)(step.step_argument)
        if(result == False):
            print("El paso "+step.basestep_name+" ha fallado.")
            Test_steps.objects.filter(test_id=test_id).delete()
            return False
        else:
            print("El paso "+step.basestep_name+" se ha completado correctamente.")
    Test_steps.objects.filter(test_id=test_id).delete()
    return True

# STEPS CLASS
# Esta clase contiene una funcion por cada paso...
class Step_Execution():
    test_id = 0
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
    
    def __init__(self, test_id): 
        self.test_id = test_id
        
    def abrir_nodo(self):
        self.driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.get('https://www.google.com')

    def reloadventana(self, argument):
        try:
            self.driver.refresh()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()
            return False

    def clickonid(self, argument):
        try:
            self.driver.find_element_by_name(argument).click()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()
            return False
    
    def esperartexto(self, argument):
        count=0
        max_tries = 10
        while True:
            if argument in self.driver.page_source:
                return True
            if count > max_tries:
                self.driver.quit()
                return False
            else:
                count+=1
                time.sleep(1)

    def escribirenid(self, argument):
        try:
            input_object = self.driver.find_element_by_name(argument)
            input_object.send_keys(argument)
            return True
        except Exception as e:
            print(e)
            self.driver.quit()
            return False

    def esperar_segundos(self, argument):
        try:
            self.driver.implicitly_wait(int(argument))
            time.sleep(int(argument))
            print("Done waiting...")
            return True
        except Exception as e:
            print(e)
            self.driver.quit()
            return False

        

    
    


    








































