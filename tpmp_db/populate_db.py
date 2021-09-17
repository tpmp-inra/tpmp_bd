import os
import random
import datetime
from datetime import datetime as dt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpmp_db.settings")

import django

django.setup()

import names

from django.db import models
from django.utils import timezone
from django.test.utils import setup_test_environment

setup_test_environment()

import dbms.models as md


TABLES = [
    md.Annotation,
    md.Person,
    md.Location,
    md.Sensor,
    md.CameraConfigurationFile,
    md.Experiment,
    md.DataIn,
    md.AnalysisResult,
    md.Plant,
    md.Measure,
    md.Weighting,
    md.Photo,
]

ORGANIZATIONS = ["CNRS", "INRAE", "ADEME", "IFREMER"]

SPECIES = ["tomato", "wheat", "sunflower", "arabidopsis"]
INTERACTIONS = ["ralsto", "myc", None, "dc3000"]
ECOTYPES = [f"ecotype_{i}" for i in range(10)]
LINES = [f"lne_{i}" for i in range(10)]
SEED_LOT = [f"seed_lot_{i}" for i in range(10)]
TYPE = ["Mutant", "WT"]


def get_random(l: list):
    return l[random.randint(0, len(l) - 1)]


for table in TABLES:
    table.objects.all().delete()


tpmp_staff = []
for _ in range(4):
    n = names.get_first_name()
    s = names.get_last_name()
    o = get_random(ORGANIZATIONS)
    person = md.Person(name=n, surname=s, mail=f"{n}.{s}@inrae.fr", affiliation=o)
    person.save()
    tpmp_staff.append(person)

researchers = []
for _ in range(5):
    n = names.get_first_name()
    s = names.get_last_name()
    o = get_random(ORGANIZATIONS)
    person = md.Person(name=n, surname=s, mail=f"{n}.{s}@{o.lower()}.fr", affiliation=o)
    person.save()
    researchers.append(person)

ancillary_staff = []
for _ in range(10):
    n = names.get_first_name()
    s = names.get_last_name()
    o = get_random(ORGANIZATIONS)
    person = md.Person(name=n, surname=s, mail=f"{n}.{s}@{o.lower()}.fr", affiliation=o)
    person.save()
    ancillary_staff.append(person)


for loc in ["Phenopsis", "Phenoserre 1", "Phenoserre 2", "RobotRacine"]:
    md.Location(label=loc, description=f"Description for {loc}").save()
locations = md.Location.objects.all()

cameras = []
for lbl, tp, mk, model_, da, st, loc, desc in zip(
    ["cam_phenopsis", "cam_vis_phenoserre", "cam_ms_phenoserre"],
    ["camera", "camera", "camera"],
    ["panasonic", "fujifilm", "sony"],
    ["mk1", "mk2", "mk3"],
    [timezone.now() + datetime.timedelta(minutes=i) for i in range(3)],
    [md.Sensor.SENSOR_STATES[random.randint(0, 4)][0] for _ in range(3)],
    [locations[i] for i in [0, 1, 2]],
    ["cam1", "cam2", "cam3"],
):
    camera = md.Sensor(
        label=lbl,
        type=tp,
        maker=mk,
        model=model_,
        date_added=da,
        state=st,
        location=loc,
        description=desc,
    )
    camera.save()
    cameras.append(camera)

scales = []
for lbl, tp, mk, model_, da, st, loc, desc in zip(
    ["scale1", "scale2", "scale3"],
    ["scale", "scale", "scale"],
    ["pierrabot", "balance", "terraillon"],
    ["mk1", "mk2", "mk3"],
    [timezone.now() + datetime.timedelta(minutes=i) for i in range(3)],
    [md.Sensor.SENSOR_STATES[random.randint(0, 4)][0] for _ in range(3)],
    [locations[i] for i in [0, 1, 2]],
    ["scale1", "scale2", "scale3"],
):
    scale = md.Sensor(
        label=lbl,
        type=tp,
        maker=mk,
        model=model_,
        date_added=da,
        state=st,
        location=loc,
        description=desc,
    )
    scale.save()
    scales.append(scale)

thermometers = []
for lbl, tp, mk, model_, da, st, loc, desc in zip(
    ["temp1", "temp2", "temp3"],
    ["thermometer", "thermometer", "thermometer"],
    ["heatmetter", "bayer", "funnytemp"],
    ["mk1", "mk2", "mk3"],
    [timezone.now() + datetime.timedelta(minutes=i) for i in range(3)],
    [md.Sensor.SENSOR_STATES[random.randint(0, 4)][0] for _ in range(3)],
    [locations[i] for i in [0, 1, 2]],
    ["temp1", "temp2", "temp3"],
):
    therm = md.Sensor(
        label=lbl,
        type=tp,
        maker=mk,
        model=model_,
        date_added=da,
        state=st,
        location=loc,
        description=desc,
    )
    therm.save()
    thermometers.append(therm)

cam_conf_files = []
for file, camera, ts, desc in zip(
    ["cam_conf_1.csv", "cam_conf_2.csv", "cam_conf_3.csv"],
    [cameras[i] for i in range(3)],
    [timezone.now() + datetime.timedelta(minutes=i) for i in range(3)],
    ["Camera configuration 1", "Camera configuration 2", "Camera configuration 3"],
):
    cf = md.CameraConfigurationFile(
        filename=file, camera=camera, timestamp=ts, description=desc
    )
    cf.save()
    cam_conf_files.append(cf)

for i in range(200):
    therm = get_random(thermometers)
    md.Measure(
        sensor=therm,
        timestamp=timezone.now() + datetime.timedelta(minutes=i),
        type=therm.type,
        label=therm.label,
        value=random.randint(12, 40),
        unit="°C",
    ).save()


experiments = []
EXP_COUNT = 26
for exp_name in [f"exp_{i}" for i in range(EXP_COUNT)]:
    camera = get_random(cameras)
    camera_settings = md.CameraConfigurationFile.objects.filter(camera__id=camera.id)[0]
    scale = get_random(scales)
    exp = md.Experiment(
        name=exp_name,
        researcher=get_random(researchers),
        referent=get_random(tpmp_staff),
        description=f"Description for {exp_name}",
        cam_settings=camera_settings,
        location=camera.location,
        species=get_random(SPECIES),
        interaction=get_random(INTERACTIONS),
        date_start=timezone.now() + datetime.timedelta(minutes=random.randint(10, 100)),
        date_end=timezone.now() + datetime.timedelta(minutes=random.randint(10, 100)),
    )
    exp.save()
    # exp.allowed_persons.add(get_random(ancillary_staff))
    exp.allowed_persons.set(
        [get_random(ancillary_staff) for _ in range(random.randint(2, 12))]
    )
    exp.save()
    for i in range(random.randint(20, 30)):
        plant = md.Plant(
            name=f"{exp.name}_p{i}",
            experiment=exp,
            species=exp.species,
            treatment=exp.interaction if (i % 2) == 0 else "control",
            ecotype=get_random(ECOTYPES),
            line=get_random(LINES),
            seed_lot=get_random(SEED_LOT),
            type=get_random(SEED_LOT),
        )
        plant.save()
        for j in range(random.randint(20, 30)):
            guid = f"guid"
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                md.Photo(
                    filename=f"{exp.name}_{plant.name}_{camera.label}_{j}_{angle}",
                    experiment=exp,
                    plant=plant,
                    camera=camera,
                    timestamp=exp.date_start + datetime.timedelta(minutes=j),
                    angle=str(angle),
                    wavelength=str(random.randint(500, 860)),
                    job_id=j,
                ).save()
            for lbl in ["initialWeight", "finalWeight", "waterPump1", "waterPump2"]:
                md.Weighting(
                    plant=plant,
                    sensor=scale,
                    timestamp=exp.date_start + datetime.timedelta(minutes=j),
                    type=scale.type,
                    label=lbl,
                    value=random.randint(100, 3000),
                    unit="kg",
                    job_id=j,
                ).save()
    experiments.append(exp)


for file, experiment, ts, desc in zip(
    [f"datain_{i}.csv" for i in range(EXP_COUNT)],
    experiments,
    [
        timezone.now() + datetime.timedelta(minutes=random.randint(0, 100))
        for _ in range(EXP_COUNT)
    ],
    [f"DATA IN {i}" for i in range(EXP_COUNT)],
):
    md.DataIn(filename=file, experiment=experiment, timestamp=ts, description=desc).save()


for file, experiment, ts, desc in zip(
    [f"ares_{i}.csv" for i in range(EXP_COUNT)],
    experiments,
    [
        timezone.now() + datetime.timedelta(minutes=random.randint(0, 100))
        for _ in range(EXP_COUNT)
    ],
    [f"Analysis result {i}" for i in range(EXP_COUNT)],
):
    md.AnalysisResult(
        filename=file, experiment=experiment, timestamp=ts, description=desc
    ).save()


tables = TABLES[:]
tables.pop(tables.index(md.Annotation))
for table in TABLES:
    items = table.objects.all()
    count = table.objects.count()
    if count == 0:
        continue
    for i in range(random.randint(1, 20)):
        item = get_random(items)
        md.Annotation(
            target_type=table.table_name(),
            target_id=item.id,
            target_class_name=table.__class__.__name__,
            level=md.Annotation.ANNOTATION_LEVELS[random.randint(0, 4)][0],
            timestamp=timezone.now() + datetime.timedelta(minutes=i),
            description=f"Annotation for {str(item)}",
        ).save()
