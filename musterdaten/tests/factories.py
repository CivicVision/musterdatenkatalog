import datetime

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

    name = 'Category'

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
    metadata_created =  datetime.date(2020, 5, 7)
    modeldataset = factory.SubFactory(ModeldatasetFactory)
    category = factory.SubFactory(CategoryFactory)
    city = factory.SubFactory(CityFactory)
    license = factory.SubFactory(LicenseFactory)


