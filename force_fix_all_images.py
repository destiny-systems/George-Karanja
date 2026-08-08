from portfolio.models import Property, UnitType, GalleryImage, Floor

for prop in Property.objects.all():
    gallery = list(GalleryImage.objects.filter(property=prop))
    if not gallery:
        print(f"SKIP {prop.name}: no gallery to pull from")
        continue

    # Fix hero image if missing
    if not prop.hero_image:
        prop.hero_image = gallery[0].image
        prop.save()
        print(f"{prop.name}: hero_image force-set")

    # Fix unit type images if missing
    units = list(UnitType.objects.filter(property=prop))
    for i, u in enumerate(units):
        if not u.image:
            u.image = gallery[i % len(gallery)].image
            u.save()
            print(f"{prop.name} - {u.name}: image force-set")

    # Fix floor images if missing
    floors = list(Floor.objects.filter(property=prop))
    fixed_floors = 0
    for i, floor in enumerate(floors):
        if not floor.image:
            floor.image = gallery[i % len(gallery)].image
            floor.save()
            fixed_floors += 1
    if fixed_floors:
        print(f"{prop.name}: {fixed_floors} floor images force-set")

print("\nDone.")
