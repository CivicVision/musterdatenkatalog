from django.utils import timezone

import factory
from musterdaten import models

"""
class Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.

    title = 'Category'
"""

class LicenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.License

    title = 'Lizenz'

class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.City

    name = 'San Diego'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    title = 'Category'

class ModelsubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Modelsubject

    title = 'Modelsubject'

class ModeldatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Modeldataset

    title = 'Modeldataset'
    modelsubject = factory.SubFactory(ModelsubjectFactory)

class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Dataset

    title = 'Interesting Dataset'
    metadata_generated_at = timezone.now()
    modeldataset = factory.SubFactory(ModeldatasetFactory)
    city = factory.SubFactory(CityFactory)
    license = factory.SubFactory(LicenseFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for category in extracted:
                self.categories.add(category)

class ScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Score

    session_id = '1234'
    dataset = factory.SubFactory(DatasetFactory)
    modeldataset = factory.SubFactory(ModeldatasetFactory)

class Top3Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Top3

    pred = 0.5
    dataset = factory.SubFactory(DatasetFactory)
    modeldataset = factory.SubFactory(ModeldatasetFactory)

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser

    ip_address = "127.0.0.1"

class DatasetWithTop3Factory(DatasetFactory):
    top_3= factory.RelatedFactory(
        Top3Factory,
        factory_related_name='dataset',
    )

