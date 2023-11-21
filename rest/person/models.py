from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class Person(models.Model):
    class Colors(models.TextChoices):
        RED = 'RED', _('Red')
        ORANGE = 'ORANGE', _('Orange')
        YELLOW = 'YELLOW', _('Yellow')
        GREEN = 'GREEN', _('Green')
        BLUE = 'BLUE', _('Blue')
        PURPLE = 'PURPLE', _('Purple')
        BLACK = 'BLACK', _('Black')
        WHITE = 'WHITE', _("White")
        BROWN = 'BROWN', _("Brown")
        BORING = 'BORING', _('None because I am boring')

    name = models.CharField(max_length=30, primary_key=True, unique=True)
    age = models.IntegerField(default=0)
    favorite_color = models.CharField(max_length=20, choices=Colors.choices, default=Colors.BORING)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
