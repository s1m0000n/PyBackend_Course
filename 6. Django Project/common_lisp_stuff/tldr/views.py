from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Function, FunctionDocument
from .serializers import FunctionSerializer
from django.shortcuts import render
from django.contrib import auth
import json


def login_required(fun):
    def wrapper(obj, request, *args, **kwargs):
        return fun(obj, request, *args, **kwargs) if request.user.is_authenticated \
            else render(request, 'main.html',
                        {'snippets': Function.objects.all(), 'user': request.user, 'from_api': True})

    return wrapper


# Create your views here.
class FunctionList(APIView):
    @login_required
    def get(self, request):
        serializer = FunctionSerializer(Function.objects.all(), many=True)
        return Response({'functions': serializer.data})

    @login_required
    def put(self, request):
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(('GET',))
def search(request):
    query = request.GET['query']
    s = FunctionDocument.search().filter('term', examples=query)
    return Response({'results': FunctionSerializer(s.to_queryset(), many=True).data})


def main_view(request):
    credentials = None
    if request.method == 'POST':
        if 'username' in request.POST:
            user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                auth.login(request, user)
            else:
                credentials = False
    return render(request, 'main.html', {'snippets': Function.objects.all()[:20],
                                         'user': request.user, 'credentials': credentials})


def logout(request):
    auth.logout(request)
    return render(request, 'main.html',
                  {'snippets': Function.objects.all()[:20], 'user': request.user})


class FunctionDetail(APIView):
    @login_required
    def get_object(self, pk):
        try:
            return Function.objects.get(pk=pk)
        except Function.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    @login_required
    def get(self, request, pk):
        return Response({'function': FunctionSerializer(self.get_object(pk)).data})

    @login_required
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_200_OK)

    @login_required
    def post(self, request, pk):
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(self.get_object(pk), serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
