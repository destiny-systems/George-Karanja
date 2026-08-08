from portfolio.models import Property, GalleryImage, UnitType, Floor

for prop in Property.objects.all():
    print(f"=== {prop.name} ===")
    print(f"  hero_image: {prop.hero_image}")
    print(f"  gallery_images count: {GalleryImage.objects.filter(property=prop).count()}")
    print(f"  unit_types count: {UnitType.objects.filter(property=prop).count()}")
    for u in UnitType.objects.filter(property=prop):
        print(f"    - {u.name}: image={u.image}")
    print(f"  floors count: {Floor.objects.filter(property=prop).count()}")
