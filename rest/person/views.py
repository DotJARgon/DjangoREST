from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from license.models import LicenseSerializer
from person.models import Person, PersonSerializer


class ListPersons(APIView):
    def get(self, request):
        people = Person.objects.all().order_by('name')
        paginator = Paginator(people, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
        serializer = PersonSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilterPersons(APIView):
    def get(self, request):
        filters = request.data['filters']
        print(request.data)
        query = Q()
        for f in filters:
            if "name" in f.keys():
                query &= Q(name__icontains=f['name'])
            elif "age" in f.keys():
                operation = f["operation"]
                if operation == "lt":
                    query &= Q(age__lt=f['age'])
                elif operation == "lte":
                    query &= Q(age__lte=f['age'])
                elif operation == "gt":
                    query &= Q(age__gt=f['age'])
                elif operation == "gte":
                    query &= Q(age__gte=f['age'])
                elif operation == "eq":
                    query &= Q(age=f['age'])
            elif "color" in f.keys():
                query &= Q(favorite_color__icontains=f['color'])
        filtered = Person.objects.filter(query)
        serializer = PersonSerializer(filtered, many=True)
        return Response(serializer.data)

class PersonLicenses(APIView):
    def get(self, request):
        persons = Person.objects.get(name=request.data['name'])
        licenses = persons.license_set.all()
        serializer = LicenseSerializer(licenses, many=True)
        return Response(serializer.data)
