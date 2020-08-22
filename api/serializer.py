from rest_framework import serializers

from musterdaten.models import Modeldataset

class ModeldatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modeldataset
        fields = ['id', 'title']
