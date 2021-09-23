from django.contrib import admin
from django.contrib.admin.decorators import display
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    Organization,
    Project,
    AnalysisProtocol,
)


class BaseInline(admin.TabularInline):
    extra = 0
    can_delete = False
    max_num = 10

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EmployeeInline(admin.StackedInline):
    model = Person
    verbose_name_plural = "person"


class ExperienceInline(BaseInline):
    model = Experiment
    verbose_name = "Experiment"
    verbose_name_plural = "Experiments"


class PlantInline(BaseInline):
    model = Plant


class OrganizationInline(BaseInline):
    model = Organization


class ProjectInline(BaseInline):
    model = Project


class PersonInline(admin.StackedInline):
    model = Person
    verbose_name_plural = "persons"


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline,)


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
        "project",
        "referent",
        "location",
        "cam_settings",
        "date_start",
        "date_end",
    )
    list_filter = ("location", "cam_settings", "referent")
    fields = [
        "name",
        "project",
        "referent",
        "location",
        "cam_settings",
        ("date_start", "date_end"),
        "description",
        "guid",
    ]
    inlines = [PlantInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "description")
    inlines = [ProjectInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "researcher",
        "organization",
        "species",
        "interaction",
    )
    list_filter = ("researcher", "organization", "species", "interaction")
    filter_horizontal = ("participants",)
    inlines = [ExperienceInline]


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


@admin.register(AnalysisProtocol)
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
    list_display = (
        "short_description_string",
        "timestamp",
        "target_type",
        "level",
    )
    list_filter = ("target_type", "level")
