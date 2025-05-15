from django.db import models
from django.utils.translation import gettext_lazy as _


class TitleChoices(models.TextChoices):
    Title = 'title', _('Select your title')
    Miss = 'miss', _('Miss')
    Mrs = 'mrs', _('Mrs')
    Mr = 'mr', _('Mr')
