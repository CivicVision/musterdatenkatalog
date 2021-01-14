from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.models import Group

from django.db.models.functions import TruncDate

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
    ScoreSummary,
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
    list_display = ("pk", "title", "scored")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _score_count=Count("score", distinct=True),
        )
        return queryset


    def scored(self, obj):
        return obj._score_count

    scored.admin_order_field = '_score_count'


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
    list_display = ("dataset", "modeldataset", "created_at", "user_id")


class NoMatchScoreAdmin(admin.ModelAdmin):
    model = NoMatchScore
    list_display = ("dataset", "session_id", "topic", "term")


class ScoreSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/score_change_list.html'
    actions = None
    show_full_result_count = False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = list(
            qs
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .order_by('date')
            .annotate(scores=Count('date'))
        )

        response.context_data['summary_total'] = dict(qs.aggregate(total=Count('pk')))

        return response



admin.site.register(ScoreSummary, ScoreSummaryAdmin)
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
