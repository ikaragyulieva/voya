from django.db import models


class TitleChoices(models.TextChoices):
    Title = 'title', 'Select your title'
    Miss = 'miss', 'Miss'
    Mrs = 'mrs', 'Mrs'
    Mr = 'mr', 'Mr'
