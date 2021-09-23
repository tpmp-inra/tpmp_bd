import sys

from django.contrib.auth.models import User

from django.db import models
from django.utils.html import linebreaks
from django.urls import reverse


class Organization(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=520)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("organization-detail", args=[str(self.id)])

    @property
    def short_description(self):
        return str(self)

    @property
    def to_string(self) -> str:
        return str(self)

    @staticmethod
    def table_name():
        return "Organization"


class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ["user"]

    def get_absolute_url(self):
        return reverse("person-detail", args=[str(self.id)])

    @property
    def short_description(self):
        return f"{str(self)} ({self.organization.name})"

    @property
    def to_string(self) -> str:
        return str(self)

    @staticmethod
    def table_name():
        return "Person"


class Location(models.Model):
    label = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ["label"]

    def get_absolute_url(self):
        return reverse("location-detail", args=[str(self.id)])

    @property
    def short_description(self):
        return f"{str(self)}"

    @staticmethod
    def table_name():
        return "Location"


class Sensor(models.Model):
    ORDERED = "ORDERED"
    ACTIVE = "ACTIVE"
    DISCARDED = "DISCARDED"
    REPAIRING = "REPAIRING"
    STORED = "STORED"

    SENSOR_STATES = [
        (ORDERED, "ORDERED"),
        (ACTIVE, "ACTIVE"),
        (DISCARDED, "DISCARDED"),
        (REPAIRING, "REPAIRING"),
        (STORED, "STORED"),
    ]

    label = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    maker = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    date_added = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=30, choices=SENSOR_STATES, default=ACTIVE)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.maker} {self.type} {self.model}"

    def get_absolute_url(self):
        return reverse("sensor-detail", args=[str(self.id)])

    class Meta:
        ordering = ["label"]

    @staticmethod
    def table_name():
        return "Sensor"


class CameraConfigurationFile(models.Model):
    filename = models.FileField(unique=True)
    camera = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Configuration for {str(self.camera)}"

    def get_absolute_url(self):
        return reverse("cameraconfigurationfile-detail", args=[str(self.id)])

    class Meta:
        ordering = ["filename"]

    def describe_config(self):
        return linebreaks(f"Configuration for {str(self.camera)}\n{self.description}")

    describe_config.allow_tags = True

    @staticmethod
    def table_name():
        return "Camera configuration file"


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    researcher = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="researcher",
    )
    participants = models.ManyToManyField(
        to=Person,
        related_name="person_experience",
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    species = models.CharField(max_length=30, blank=True, null=True)
    interaction = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("project-detail", args=[str(self.id)])

    @property
    def short_description(self):
        return f"{str(self)}"

    @staticmethod
    def table_name():
        return "Project"


class Experiment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    referent = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    cam_settings = models.ForeignKey(
        CameraConfigurationFile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["date_start"]

    def get_absolute_url(self):
        return reverse("experiment-detail", args=[str(self.id)])

    @staticmethod
    def table_name():
        return "Experiment"


class DataIn(models.Model):
    filename = models.FileField(unique=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Data-in {self.filename}"

    def get_absolute_url(self):
        return reverse("datain-detail", args=[str(self.id)])

    class Meta:
        ordering = ["timestamp"]

    @property
    def short_description(self):
        exp = Experiment.objects.filter(id=self.experiment.id)[0]
        if exp is None:
            return f"{str(self)} no linked experiment"
        else:
            return f"{str(self)} for experiment {exp.name}"

    @staticmethod
    def table_name():
        return "Data in"


class AnalysisResult(models.Model):
    filename = models.FileField(unique=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Data-in {self.filename}"

    def get_absolute_url(self):
        return reverse("analysisresult-detail", args=[str(self.id)])

    class Meta:
        ordering = ["filename"]

    @staticmethod
    def table_name():
        return "Analysis result CSV file"


class AnalysisProtocol(models.Model):
    filename = models.FileField(unique=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["filename"]

    def get_absolute_url(self):
        return reverse("analysisprotocol-detail", args=[str(self.id)])

    @staticmethod
    def table_name():
        return "Analysis protocols"


class Plant(models.Model):
    name = models.CharField(max_length=30, unique=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    species = models.CharField(max_length=30, blank=True, null=True)
    ecotype = models.CharField(max_length=30, blank=True, null=True)
    line = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    seed_lot = models.CharField(max_length=30, blank=True, null=True)
    treatment = models.CharField(max_length=30, blank=True, null=True)

    def to_string(self) -> str:
        return f"{self.name}, {self.species}, {self.ecotype}, {self.treatment}"

    def get_absolute_url(self):
        return reverse("plant-detail", args=[str(self.id)])

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def table_name():
        return "Plant"


class Measure(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    value = models.FloatField()
    unit = models.CharField(max_length=30)
    job_id = models.IntegerField(default=-1)

    def get_absolute_url(self):
        return reverse("measure-detail", args=[str(self.id)])

    class Meta:
        ordering = ["label"]

    @staticmethod
    def table_name():
        return "Measure"


class Weighting(models.Model):
    plant = models.ForeignKey(Plant, blank=True, null=True, on_delete=models.SET_NULL)
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    value = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=30)
    job_id = models.IntegerField(default=-1)

    def get_absolute_url(self):
        return reverse("weighting-detail", args=[str(self.id)])

    class Meta:
        ordering = ["label"]

    @staticmethod
    def table_name():
        return "Measure"


class Photo(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    camera = models.ForeignKey(
        Sensor,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    timestamp = models.DateTimeField()
    filename = models.FileField(unique=True)
    angle = models.CharField(max_length=30)
    wavelength = models.CharField(max_length=30)
    job_id = models.IntegerField(default=-1)

    def get_absolute_url(self):
        return reverse("photo-detail", args=[str(self.id)])

    class Meta:
        ordering = ["filename"]

    @staticmethod
    def table_name():
        return "Photo"


thismodule = sys.modules[__name__]


class Annotation(models.Model):

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    ANNOTATION_LEVELS = [
        (DEBUG, "DEBUG"),
        (INFO, "INFO"),
        (WARNING, "WARNING"),
        (ERROR, "ERROR"),
        (CRITICAL, "CRITICAL"),
    ]

    target_type = models.CharField(max_length=100, default="Unknown")
    target_id = models.IntegerField(default=-1)
    level = models.CharField(max_length=30, choices=ANNOTATION_LEVELS, default=INFO)
    timestamp = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    target_class_name = models.CharField(max_length=100, default="Unknown")

    def __str__(self) -> str:
        return f"Annotation for {str(self.get_target_object())}"

    def get_absolute_url(self):
        return reverse("annotation-detail", args=[str(self.id)])

    def get_target_object(self):
        target_object = (getattr(thismodule, self.target_class_name)).objects.filter(
            id=self.target_id
        )[0]
        return target_object

    def short_description_string(self):
        return str(self)

    @property
    def short_description(self):
        return str(self)

    class Meta:
        ordering = ["timestamp"]

    @staticmethod
    def table_name():
        return "Annotation"
