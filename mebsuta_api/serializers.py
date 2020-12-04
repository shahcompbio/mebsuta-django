from django.contrib.auth.models import User, Group
from rest_framework import serializers
from mebsuta_api.models import Annotation, Cell_Image, Debris, Library, Mebsuta_Users


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class Cell_ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell_Image
        fields = '__all__'


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell_Image
        fields = ['library_id', "cell_id", "row", "col", "annotation"]


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'


class CellsAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["cell_id",
                  "annotation"]


class DebrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debris
        fields = '__all__'

# https://stackoverflow.com/questions/31920853/aggregate-and-other-annotated-fields-in-django-rest-framework-serializers


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class Mebsuta_UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mebsuta_Users
        fields = '__all__'
