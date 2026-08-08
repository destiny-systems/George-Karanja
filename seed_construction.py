import os
from django.core.files import File
from portfolio.models import Property, GalleryImage

percentages = {
    "GK Luxurious Residence": 85,
    "Lewis Residence": 70,
    "Cadillac Residence Kenya": 55,
}

folder = "sample_images/construction"
files = sorted(os.listdir(folder))

for prop in Property.objects.all():
    prop.construction_percent = percentages.get(prop.name, 60)
    prop.save()

    created = 0
    for i, filename in enumerate(files):
        if GalleryImage.objects.filter(property=prop, image__icontains=filename).exists():
            continue
        filepath = os.path.join(folder, filename)
        with open(filepath, 'rb') as f:
            img = GalleryImage(property=prop, room_type='construction', caption='Construction Progress')
            img.image.save(f"{prop.slug}_{filename}", File(f), save=True)
        created += 1

    print(f"{prop.name}: {prop.construction_percent}% complete, {created} construction photos added")

print("Done.")
