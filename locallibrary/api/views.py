from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from catalog.models import (Author,Book,BookInstance,Genre)
from .serializers import BookSerializer


@api_view()
def getBook(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addBook(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)