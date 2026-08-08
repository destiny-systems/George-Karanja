from portfolio.models import Property, Floor, GalleryImage

total = 0
for prop in Property.objects.all():
    gallery = list(GalleryImage.objects.filter(property=prop))
    if not gallery:
        print(f"SKIP {prop.name}: no gallery images to pull from")
        continue

    floors = list(Floor.objects.filter(property=prop))
    updated = 0
    for i, floor in enumerate(floors):
        floor.image = gallery[i % len(gallery)].image
        floor.save()
        updated += 1
    print(f"{prop.name}: set images on {updated} floors")
    total += updated

print(f"\nDone. Total floors updated: {total}")
