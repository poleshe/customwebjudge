from django.db import models
from django.contrib.postgres.fields import ArrayField

# Modelos BD webjudge.

# Contiene los usuarios de la web.
class Users(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    tests_done = ArrayField(models.CharField(max_length=255), null=True)

# Contiene información general sobre los tests.
class Tests(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    test_description = models.CharField(max_length=255)
    test_file_name = models.CharField(max_length=255)
    test_tries = models.IntegerField()

# Resultados de los tests.
class Test_results(models.Model):
    user_id = models.CharField(max_length=255)
    test_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    step_failed = models.CharField(max_length=255, null=True)
    date = models.DateField()

# Contiene los pasos de los tests.
class Test_steps(models.Model):
    test_id = models.CharField(max_length=255)
    basestep_id = models.CharField(max_length=255)
    basestep_name = models.CharField(max_length=255)
    step_argument = models.CharField(max_length=255, null=True)
    step_number = models.IntegerField()
    step_description = models.CharField(max_length=255)

# Contiene una lista con todos los pasos disponibles.
class Base_steps(models.Model):
    step_id = models.AutoField(primary_key=True)
    step_name =  models.CharField(max_length=255)
    step_description =  models.CharField(max_length=255)
    step_hasargument = models.IntegerField()
