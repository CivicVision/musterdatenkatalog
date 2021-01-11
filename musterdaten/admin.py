from django.contrib import admin
from django.contrib.auth.models import Group

from musterdaten.models import (
    Score,
    Dataset,
    City,
    Category,
    License,
    State,
    Modeldataset,
    Modelsubject,
    Leika,
    Top3,
    NoMatchScore,
    CustomUser,
)

class Top3tInline(admin.TabularInline):
    model = Top3
    extra = 3


class ScoreInlineAdmin(admin.StackedInline):
    model = Score


class DatasetAdmin(admin.ModelAdmin):
    search_fields = ("title", )
    inlines = (Top3tInline,)
    list_filter = ("modeldataset__modelsubject", "modeldataset",)


class ModeldatasetInline(admin.StackedInline):
    model = Modeldataset


class ModelsubjectAdmin(admin.ModelAdmin):
    inlines = (ModeldatasetInline,)


class CustomUserAdmin(admin.ModelAdmin):
     model = CustomUser
     list_display = ("pk", "ip_address")
     inlines = (ScoreInlineAdmin, )

    
class ScoreInlineAdmin(admin.StackedInline):
     model = Score


class ModeldatasetAdmin(admin.ModelAdmin):
    model = Modeldataset
    list_filter = ("modelsubject", )
    search_fields = ("title", )
    inlines = (ScoreInlineAdmin, )


class ScoreAdmin(admin.ModelAdmin):
    model = Score
    list_display = ("dataset", "modeldataset", "session_id")


class NoMatchScoreAdmin(admin.ModelAdmin):
    model = NoMatchScore
    list_display = ("dataset", "session_id", "topic", "term")



admin.site.unregister(Group)
admin.site.register(Score, ScoreAdmin)
admin.site.register(NoMatchScore, NoMatchScoreAdmin)
admin.site.register(Dataset, DatasetAdmin)

admin.site.register(City)
admin.site.register(Category)
admin.site.register(License)
admin.site.register(Modeldataset, ModeldatasetAdmin)
admin.site.register(State)
admin.site.register(Modelsubject, ModelsubjectAdmin)
admin.site.register(Leika)
admin.site.register(CustomUser, CustomUserAdmin)
