import os
from django.core.files import File
from portfolio.models import Property, GalleryImage

category_map = {
    'living': ('living_room', 'Living Room'),
    'kitchen': ('kitchen', 'Kitchen'),
    'bedroom': ('bedroom', 'Bedroom'),
    'bathroom': ('bathroom', 'Bathroom'),
}

folder_property_map = {
    'sample_images/gk': 'GK Luxurious Residence',
    'sample_images/lewis': 'Lewis Residence',
    'sample_images/gallery': 'Cadillac Residence Kenya',
}

total_created = 0
for folder, property_name in folder_property_map.items():
    if not os.path.isdir(folder):
        print(f"SKIP: folder not found: {folder}")
        continue

    try:
        prop = Property.objects.get(name=property_name)
    except Property.DoesNotExist:
        print(f"SKIP: Property not found: {property_name}")
        continue

    created = 0
    for filename in sorted(os.listdir(folder)):
        if filename == 'hero.jpg':
            filepath = os.path.join(folder, filename)
            with open(filepath, 'rb') as f:
                prop.hero_image.save(filename, File(f), save=True)
            print(f"  Set hero image for {property_name}")
            continue

        prefix = filename.split('_')[0]
        if prefix not in category_map:
            continue
        room_type, label = category_map[prefix]

        if GalleryImage.objects.filter(property=prop, image__icontains=filename).exists():
            continue

        filepath = os.path.join(folder, filename)
        with open(filepath, 'rb') as f:
            img = GalleryImage(property=prop, room_type=room_type, caption=label)
            img.image.save(filename, File(f), save=True)
        created += 1

    print(f"{property_name}: added {created} gallery images")
    total_created += created

print(f"\nDone. Total gallery images added: {total_created}")
