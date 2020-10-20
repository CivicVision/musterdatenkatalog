from django.contrib import admin
from django.contrib.auth.models import Group

from musterdaten.models import Score, Dataset, City, Category, License, State, Modeldataset, Modelsubject, Leika, Top3

class Top3tInline(admin.TabularInline):
    model = Top3
    extra = 3


class DatasetAdmin(admin.ModelAdmin):
    inlines = (Top3tInline,)



admin.site.unregister(Group)
admin.site.register(Score)
admin.site.register(Dataset, DatasetAdmin)

admin.site.register(City)
admin.site.register(Category)
admin.site.register(License)
admin.site.register(Modeldataset)
admin.site.register(State)
admin.site.register(Modelsubject)
admin.site.register(Leika)

