from rest_framework import serializers

from musterdaten.models import (
    Modeldataset,
    Modelsubject,
    Score,
    Dataset
)

class ModelsubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelsubject
        fields = ['id', 'title']

class ModeldatasetSerializer(serializers.ModelSerializer):
    modelsubject = ModelsubjectSerializer(many=False)
    class Meta:
        model = Modeldataset
        fields = ['id', 'title', 'modelsubject', 'name']

class ScoreSerializer(serializers.ModelSerializer):
    modeldataset = ModeldatasetSerializer(many=False, read_only=True)

    dataset_id = serializers.CharField(write_only=True)
    modeldataset_id = serializers.CharField(write_only=True)

    class Meta:
        model = Score
        fields = ['id', 'session_id', 'modeldataset',
                  'dataset_id', 'modeldataset_id']

class DatasetSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    license = serializers.StringRelatedField()
    modeldataset = serializers.StringRelatedField()
    modeldataset_id = serializers.PrimaryKeyRelatedField(queryset=Modeldataset.objects.all())
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'url', 'original_id',
                  'modeldataset', 'modeldataset_id', 'city', 'license', 'categories']

