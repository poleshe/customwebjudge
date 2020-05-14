from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
from webjudge.models import *

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