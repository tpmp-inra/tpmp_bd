from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from crispy_forms.helper import FormHelper


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


def index(request):
    return render(
        request=request,
        template_name="index.html",
        context={
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ExperimentListView, self).get_context_data(**kwargs)
        context["h1title"] = "Experiment List"
        context["objecttype"] = "experiment"
        return context


class ExperimentDetailView(generic.DetailView):
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(ExperimentDetailView, self).get_context_data(**kwargs)
        context["allowed_persons"] = context["experiment"].allowed_persons.all()
        context["plants"] = context["experiment"].plant_set.all()
        return context


class PersonListView(generic.ListView):
    model = Person

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PersonListView, self).get_context_data(**kwargs)
        context["h1title"] = "Person List"
        context["objecttype"] = "person"
        return context


class PersonDetailView(generic.DetailView):
    model = Person
