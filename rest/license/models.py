from django.db import models
from rest_framework import serializers

from person.models import Person


class License(models.Model):
    license_number = models.IntegerField(unique=True)
    license_type = models.CharField(max_length=30)
    date_made = models.DateField(auto_now_add=True)
    # person = models.ForeignKey(Person, related_name='card_holder', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('license_type', 'person')


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = ['license_number', 'license_type', 'date_made', 'person']

