from django.contrib import admin
from django.contrib.admin.decorators import display

from .models import (
    Annotation,
    Person,
    Location,
    Sensor,
    CameraConfigurationFile,
    Experiment,
    DataIn,
    AnalysisResult,
    Plant,
    Measure,
    Weighting,
    Photo,
)


class ExperienceReferentInline(admin.TabularInline):
    model = Experiment
    fk_name = "referent"
    extra = 0
    filter_horizontal = ("allowed_persons",)
    exclude = ("date_start", "date_end", "description", "allowed_persons", "guid")
    can_delete = False
    verbose_name = "Referent in experience"
    verbose_name_plural = "Referent in experiences"
    max_num = 10

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ExperienceResearcherInline(admin.TabularInline):
    model = Experiment
    fk_name = "researcher"
    extra = 0
    filter_horizontal = ("allowed_persons",)
    exclude = ("date_start", "date_end", "description", "allowed_persons", "guid")
    can_delete = False
    verbose_name = "Researcher in experience"
    verbose_name_plural = "Researcher in experiences"
    max_num = 10

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PlantInline(admin.TabularInline):
    model = Plant
    extra = 0
    max_num = 10

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "mail", "affiliation")
    list_filter = ("affiliation",)
    fields = [("name", "surname"), "mail", "affiliation"]
    inlines = [ExperienceReferentInline, ExperienceResearcherInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("label",)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("label", "type", "maker", "model", "state", "location", "date_added")
    list_filter = ("type", "maker", "state", "location")


@admin.register(CameraConfigurationFile)
class CameraConfigurationFileAdmin(admin.ModelAdmin):
    list_display = ("camera", "filename", "timestamp")
    list_filter = ("camera",)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "researcher",
        "referent",
        "location",
        "cam_settings",
        "species",
        "interaction",
        "date_start",
        "date_end",
    )
    list_filter = (
        "location",
        "species",
        "interaction",
        "cam_settings",
        "researcher",
        "referent",
    )
    fields = [
        "name",
        ("researcher", "referent"),
        "location",
        "cam_settings",
        ("species", "interaction"),
        "allowed_persons",
        ("date_start", "date_end"),
        "description",
        "guid",
    ]
    filter_horizontal = ("allowed_persons",)
    inlines = [PlantInline]


@admin.register(DataIn)
class DataInAdmin(admin.ModelAdmin):
    list_display = (
        "experiment",
        "filename",
        "timestamp",
    )


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        "experiment",
        "filename",
        "timestamp",
    )
    list_filter = ("experiment",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "experiment",
        "species",
        "ecotype",
        "line",
        "type",
        "seed_lot",
        "treatment",
    )
    list_filter = (
        "experiment",
        "species",
        "ecotype",
        "line",
        "type",
        "seed_lot",
        "treatment",
    )


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("sensor", "type", "label", "value", "unit", "timestamp")


@admin.register(Weighting)
class WeightingAdmin(admin.ModelAdmin):
    list_display = ("plant", "sensor", "type", "label", "value", "unit", "timestamp")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "plant",
        "experiment",
        "angle",
        "wavelength",
        "timestamp",
    )


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("target_id", "target_type", "level")
