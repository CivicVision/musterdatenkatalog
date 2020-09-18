from rest_framework import serializers

from django.utils import timezone
from django.utils.timezone import make_aware

from musterdaten import services

from musterdaten.models import (
    Modeldataset,
    Modelsubject,
    Score,
    Dataset,
    City,
    License,
    Category
)

class ModelsubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelsubject
        fields = ['id', 'title']

class ModeldatasetSerializer(serializers.ModelSerializer):
    modelsubject = ModelsubjectSerializer(many=False)
    class Meta:
        model = Modeldataset
        fields = ['id', 'title', 'modelsubject', 'name', 'datasets']

class ScoreSerializer(serializers.ModelSerializer):
    modeldataset = ModeldatasetSerializer(many=False, read_only=True)

    dataset_id = serializers.CharField(write_only=True)
    modeldataset_id = serializers.CharField(write_only=True)

    class Meta:
        model = Score
        fields = ['id', 'session_id', 'modeldataset',
                  'dataset_id', 'modeldataset_id']

class CategorySerializer(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value.title

    class Meta:
        model = Category


class CitySerializer(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value.name

    class Meta:
        model = City


class LicenseSerializer(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value.title

    class Meta:
        model = License

class BaseDatasetSerializer(serializers.ModelSerializer):
        # Do not instantiate this class directly. Use DatasetSerializer or CreateDatasetSerializer instead

    city = CitySerializer(many=False, queryset=City.objects.all())
    license = LicenseSerializer(many=False, queryset=License.objects.all())
    categories = CategorySerializer(many=True, queryset=Category.objects.all())


class DatasetSerializer(BaseDatasetSerializer):
    modeldataset_id = serializers.PrimaryKeyRelatedField(queryset=Modeldataset.objects.all())
    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'url', 'original_id',
                  'modeldataset',  'city', 'license', 'categories', 'modeldataset_id']

class CreateDatasetSerializer(BaseDatasetSerializer):
    modeldataset = serializers.CharField(write_only=True)
    modelsubject = serializers.CharField(write_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'url', 'original_id',
                  'modeldataset',  'city', 'license', 'categories', 'modelsubject']

    def create(self, validated_data):
        data = {
            "dataset_title": validated_data.pop("title"),
            "dataset_description": validated_data.pop("description"),
            "dataset_original_id": validated_data.pop("original_id"),
            "dataset_url": validated_data.pop("url")
        }
        if not data.get("dataset_metadata_updated_at") or data.get("dataset_metadata_updated_at") == "":
            data["dataset_metadata_updated_at"] = timezone.now()
        else:
            data["dataset_metadata_updated_at"] = make_aware(
                datetime.datetime.strptime(
                    data["dataset_metadata_updated_at"], '%Y-%m-%dT%H:%M:%S.%f')
            )

        data["modeldataset_title"] = validated_data.pop("modeldataset")
        data["modelsubject_title"] = validated_data.pop("modelsubject")

        data["city_name"] = validated_data.pop("city")
        data["license_title"] = validated_data.pop("license")
        data["categories_titles"] = validated_data.pop("categories")

        return services.create_all_models(data)
