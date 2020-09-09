from rest_framework import serializers

from musterdaten.models import Modeldataset, Modelsubject

class ModelsubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelsubject
        fields = ['id', 'title']

class ModeldatasetSerializer(serializers.ModelSerializer):
    modelsubject = ModelsubjectSerializer(many=False)
    class Meta:
        model = Modeldataset
        fields = ['id', 'title', 'modelsubject', 'name']


