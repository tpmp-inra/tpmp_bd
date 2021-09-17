from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("experiments/", views.ExperimentListView.as_view(), name="experiments"),
    path(
        "experiment/<int:pk>",
        views.ExperimentDetailView.as_view(),
        name="experiment-detail",
    ),
    path("persons/", views.PersonListView.as_view(), name="persons"),
    path(
        "person/<int:pk>",
        views.PersonDetailView.as_view(),
        name="person-detail",
    ),
]
