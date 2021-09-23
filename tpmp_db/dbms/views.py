from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

# from crispy_forms.helper import FormHelper


from .models import (
    AnalysisProtocol,
    Annotation,
    Person,
    Location,
    Project,
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
)


PAGINATE_BY = 20


def index(request):
    return render(
        request=request,
        template_name="index.html",
        context={
            "num_org": Organization.objects.all().count(),
            "num_project": Project.objects.all().count(),
            "num_exp": Experiment.objects.all().count(),
            "num_plant": Plant.objects.all().count(),
            "num_measure": Measure.objects.all().count(),
            "num_photo": Photo.objects.all().count(),
            "num_person": Person.objects.all().count(),
            "num_anres": AnalysisResult.objects.all().count(),
            "num_cam_conf": CameraConfigurationFile.objects.all().count(),
            "num_datain": DataIn.objects.all().count(),
            "num_weighting": Weighting.objects.all().count(),
            "num_locations": Location.objects.all().count(),
            "num_sensor": Sensor.objects.all().count(),
            "num_anno": Annotation.objects.all().count(),
        },
    )


class ExperimentListView(generic.ListView):
    model = Experiment
    paginate_by = PAGINATE_BY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ExperimentListView, self).get_context_data(**kwargs)
        context["h1title"] = "List of experiments"
        context["objecttype"] = "experiment"
        return context


class ExperimentDetailView(generic.DetailView):
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(ExperimentDetailView, self).get_context_data(**kwargs)
        context["participants"] = context["experiment"].project.participants.all()
        context["plants"] = context["experiment"].plant_set.all()
        return context


class PersonListView(generic.ListView):
    model = Person
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PersonListView, self).get_context_data(**kwargs)
        context["h1title"] = "List of persons"
        context["objecttype"] = "person"
        return context


class PersonDetailView(generic.DetailView):
    model = Person

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        return context


class LocationListView(generic.ListView):
    model = Location
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(LocationListView, self).get_context_data(**kwargs)
        context["h1title"] = "List of locations"
        context["objecttype"] = "location"
        return context


class LocationDetailView(generic.DetailView):
    model = Location


class DataInListView(generic.ListView):
    model = DataIn
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DataInListView, self).get_context_data(**kwargs)
        context["kind"] = "Data ins"
        return context


class DataInDetailView(generic.DetailView):
    model = DataIn

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DataInDetailView, self).get_context_data(**kwargs)
        context["experiment"] = Experiment.objects.filter(
            id=context["datain"].experiment_id
        )[0]
        context["kind"] = "Data in"
        context["object_detail"] = context["datain"]
        return context


class AnalysisResultListView(generic.ListView):
    model = AnalysisResult
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(AnalysisResultListView, self).get_context_data(**kwargs)
        context["kind"] = "Analysis results"
        return context


class AnalysisResultDetailView(generic.DetailView):
    model = AnalysisResult

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(AnalysisResultDetailView, self).get_context_data(**kwargs)
        context["experiment"] = Experiment.objects.filter(
            id=context["analysisresult"].experiment_id
        )[0]
        context["kind"] = "analysis result"
        context["object_detail"] = context["analysisresult"]
        return context


class AnalysisProtocolListView(generic.ListView):
    model = AnalysisProtocol
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(AnalysisProtocolListView, self).get_context_data(**kwargs)
        context["kind"] = "analysis protocols"
        return context


class AnalysisProtocolDetailView(generic.DetailView):
    model = AnalysisProtocol

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(AnalysisProtocolDetailView, self).get_context_data(**kwargs)
        context["experiment"] = Experiment.objects.filter(
            id=context["analysisprotocol"].experiment_id
        )[0]
        context["kind"] = "analysis protocol"
        context["object_detail"] = context["analysisprotocol"]
        return context


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = PAGINATE_BY


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["participants"] = context["project"].participants.all()
        context["experiments"] = context["project"].experiment_set.all()
        return context


class OrganizationListView(generic.ListView):
    model = Organization
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context["h1title"] = "List of organizations"
        context["objecttype"] = "organization"
        return context


class OrganizationDetailView(generic.DetailView):
    model = Organization

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context["projects"] = context["organization"].project_set.all()
        return context


class SensorListView(generic.ListView):
    model = Sensor
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SensorListView, self).get_context_data(**kwargs)
        context["h1title"] = "List of sensors"
        context["objecttype"] = "sensor"
        return context


class SensorDetailView(generic.DetailView):
    model = Sensor

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(SensorDetailView, self).get_context_data(**kwargs)
        context["ccfs"] = context["sensor"].cameraconfigurationfile_set.all()
        return context


class CameraConfigurationFileListView(generic.ListView):
    model = CameraConfigurationFile
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CameraConfigurationFileListView, self).get_context_data(**kwargs)
        context["kind"] = "analysis protocols"
        return context


class CameraConfigurationFileDetailView(generic.DetailView):
    model = CameraConfigurationFile

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CameraConfigurationFileDetailView, self).get_context_data(
            **kwargs
        )
        context["experiments"] = context["cameraconfigurationfile"].experiment_set.all()
        return context


class PlantListView(generic.ListView):
    model = Plant
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PlantListView, self).get_context_data(**kwargs)
        return context


class PlantDetailView(generic.DetailView):
    model = Plant

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PlantDetailView, self).get_context_data(**kwargs)
        context["photos"] = context["plant"].photo_set.all()
        return context
