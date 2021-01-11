from django.db import models
from django.db.models import Avg, Sum


class Modelsubject(models.Model):
    title = models.CharField(max_length=64, verbose_name="titel")

    def first_letter(self):
        return self.title and self.title[0] or ''

    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "Themen"
        ordering = ['title']

    def __str__(self):
        return self.title


class Leika(models.Model):
    title = models.CharField(max_length=64, verbose_name="titel")
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Modeldataset(models.Model):
    title = models.CharField(max_length=128, verbose_name="titel")

    modelsubject = models.ForeignKey(to=Modelsubject, on_delete=models.PROTECT)
    leika = models.ForeignKey(to=Leika, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Musterdatensatz'
        verbose_name_plural = 'Musterdatensätze'
        ordering = ['title']

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.modelsubject.title + " - " + self.title


class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name="titel")
    DCAT_AP = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    def __str__(self):
        return self.title


class License(models.Model):
    title = models.CharField(max_length=128, verbose_name="titel")
    url = models.URLField()
    short_title = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Lizenz"
        verbose_name_plural = "Lizenzen"

    def __str__(self):
        return self.title


class State(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Bundesland"
        verbose_name_plural = "Bundesländer"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Stadt"
        verbose_name_plural = "Städte"

    def __str__(self):
        return self.name


class Dataset(models.Model):
    title = models.CharField(max_length=512, verbose_name="titel")
    description = models.TextField(verbose_name="beschreibung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="erstellt_am")
    original_id = models.CharField(max_length=512, verbose_name="portal_id")
    url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True, verbose_name="geändert_am")
    metadata_updated_at = models.DateTimeField(verbose_name="metadaten_geändert_am", null=True)
    metadata_generated_at = models.DateTimeField(verbose_name="metadaten_generiert", null=True)

    modeldataset = models.ForeignKey(to=Modeldataset, on_delete=models.PROTECT, related_name="datasets")
    city = models.ForeignKey(to=City, on_delete=models.PROTECT)
    license = models.ForeignKey(to=License, on_delete=models.PROTECT)

    categories = models.ManyToManyField(to=Category)
    top_3 = models.ManyToManyField(to=Modeldataset, through="Top3")

    class Meta:
        verbose_name = 'Datensatz'
        verbose_name_plural = 'Datensätze'
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def top3_modelsubjects(self):
        return [Top3Modelsubject(t) for t in self.get_top3_modelsubjects().all()]

    @property
    def top3_modeldatasets(self):
        return top3

    def top3_modeldatasets_by_modelsubject(self, modelsubject_id):
        objects = self.get_top3_modeldatasets().filter(modeldataset__modelsubject__id=modelsubject_id).all()
        return [Top3Modeldataset(o) for o in objects]

    def get_top3_modeldatasets(self):
        return Top3.objects.filter(dataset_id=self.pk).select_related().values(
            'modeldataset_id',
            'modeldataset__title',
        ).annotate(pred=Avg('pred')).order_by('-pred')

    def get_top3_modelsubjects(self):
        return Top3.objects.filter(dataset_id=self.pk).select_related().values(
            'modeldataset__modelsubject__id',
            'modeldataset__modelsubject__title',
        ).annotate(pred=Sum('pred')).order_by('-pred')


class Score(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    dataset = models.ForeignKey(to=Dataset, on_delete=models.PROTECT)
    modeldataset = models.ForeignKey(to=Modeldataset, on_delete=models.PROTECT)
    session_id = models.CharField(max_length=32)
    user = models.ForeignKey(to="CustomUser", on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = "Bewertung"
        verbose_name_plural = "Bewertungen"
        ordering = ['id']

    def __str__(self):
        return "Dataset: " + self.dataset.title + " - Musterdatensatz: " + self.modeldataset.title


class Top3(models.Model):
    dataset = models.ForeignKey(
        to=Dataset, on_delete=models.PROTECT, related_name="top3_modeldatasets")
    modeldataset = models.ForeignKey(to=Modeldataset, on_delete=models.PROTECT)
    pred = models.FloatField()

class Prediction():
    @property
    def prediction_percentage(self):
        return 100 if self.pred > 1 else round(self.pred * 100)


class Top3Modelsubject(Prediction):
    def __init__(self,entry):
        self.pk = entry.get('modeldataset__modelsubject__id')
        self.title = entry.get('modeldataset__modelsubject__title')
        self.pred = entry.get('pred')


class Top3Modeldataset(Prediction):
    def __init__(self,entry):
        self.pk = entry.get('modeldataset_id')
        self.title = entry.get('modeldataset__title')
        self.pred = entry.get('pred')

class NoMatchScore(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     dataset = models.ForeignKey(to=Dataset, on_delete=models.PROTECT)
     session_id = models.CharField(max_length=32)
     topic = models.CharField(max_length=255)
     term = models.CharField(max_length=255)

     class Meta:
         ordering = ['id']

     def __str__(self):
         return "Dataset: " + self.dataset.title + " - Musterdatensatz: " + self.text

class CustomUser(models.Model):
     ip_address = models.CharField(max_length=100)
