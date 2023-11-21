from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from license.models import License, LicenseSerializer


class ListLicense(APIView):
    def get(self, request):
        licenses = License.objects.all()

        serializer = LicenseSerializer(licenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = LicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        print(request.data)
        License.objects.filter(license_number=request.data['license_number']).delete()
        return Response(f'deleted {request.data["license_number"]}', status=status.HTTP_200_OK)
