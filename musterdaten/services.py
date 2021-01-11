import datetime

from django.utils import timezone
from django.utils.timezone import make_aware

from musterdaten.models import Category, Dataset, Modeldataset, Modelsubject, License, City


def read_row(row):
    data = {}
    data["dataset_title"] = row[0]
    data["dataset_description"] = row[4]
    data["dataset_original_id"] = row[5]

    if row[8] == "":
        data["dataset_metadata_updated_at"] = timezone.now()
    else:
        data["dataset_metadata_updated_at"] = make_aware(
            datetime.datetime.strptime(row[8], '%Y-%m-%dT%H:%M:%S.%f')
        )

    data["dataset_metadata_generated_at"] = timezone.now()
    data["dataset_url"] = row[10]

    data["modelsubject_title"] = row[2]
    data["modeldataset_title"] = row[3]
    data["license_title"] = row[6]
    data["categories_titles"] = row[7].split(",")
    data["city_name"] = row[9]

    return data



def create_all_models(data):
    if not data:
        return

    city, _ = City.objects.get_or_create(name=data.get("city_name"))
    license, _ = License.objects.get_or_create(title=data.get("license_title"))
    modelsubject, _ = Modelsubject.objects.get_or_create(title=data.get("modelsubject_title"))
    modeldataset, _ = Modeldataset.objects.get_or_create(
            title=data.get("modeldataset_title"),
            modelsubject=modelsubject
            )

    dataset, _ = Dataset.objects.get_or_create(
            title=data.get("dataset_title"),
            description=data.get("dataset_description"),
            original_id=data.get("dataset_original_id"),
            metadata_updated_at=data.get("dataset_metadata_updated_at", ),
            metadata_generated_at=data.get("dataset_metadata_generated_at", ),
            url=data.get("dataset_url"),
            modeldataset=modeldataset,
            city=city,
            license=license
            )

    for category_title in data.get("categories_titles"):
        category, _ = Category.objects.get_or_create(title=category_title)
        dataset.categories.add(category)

    return dataset



def update_models(data):
    if not data:
        return

    city = City.objects.filter(name=data.get("city_name")).first()
    dataset = Dataset.objects.filter(original_id=data.get("dataset_original_id"), city=city).all()

    if not dataset:
        return

    license, _ = License.objects.get_or_create(title=data.get("license_title"))

    dataset.update(
            title=data.get("dataset_title"),
            description=data.get("dataset_description"),
            metadata_updated_at=data.get("dataset_metadata_updated_at", ),
            metadata_generated_at=data.get("dataset_metadata_generated_at", ),
            url=data.get("dataset_url"),
            license=license
    )

    return dataset
