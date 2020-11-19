# from django.shortcuts import render
# from django.http import HttpResponse
# import django.db as db
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Function
from .serializers import FunctionSerializer


# Create your views here.
class FunctionList(APIView):
    def get(self, request):
        functions = Function.objects.all()
        serializer = FunctionSerializer(functions, many=True)
        return Response({'functions': serializer.data})

    def put(self, request):
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FunctionDetail(APIView):
    def get_object(self, pk):
        try:
            return Function.objects.get(pk=pk)
        except Function.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk):
        function = self.get_object(pk)
        serializer = FunctionSerializer(function)
        return Response({'function': serializer.data})

    def delete(self, request, pk):
        function = self.get_object(pk)
        function.delete()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk):
        function = self.get_object(pk)
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(function, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)