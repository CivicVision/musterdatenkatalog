from musterdaten.models import Category, Dataset, Modeldataset, Modelsubject, License, City

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
