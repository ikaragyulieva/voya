from django.db import models


class AccountTypeChoices(models.TextChoices):
    Employee = 'employee', 'Employee'
    Client = 'client', 'Client'

