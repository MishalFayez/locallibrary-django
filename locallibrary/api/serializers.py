from rest_framework import serializers
from catalog.models import (Author,Book,BookInstance,Genre)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'