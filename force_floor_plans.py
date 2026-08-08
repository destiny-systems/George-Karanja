from portfolio.models import Property, Floor, GalleryImage

for prop in Property.objects.all():
    gallery = list(GalleryImage.objects.filter(property=prop))
    if not gallery:
        continue
    floors = list(Floor.objects.filter(property=prop, floor_plan_image=''))
    for i, floor in enumerate(floors):
        floor.floor_plan_image = gallery[(i + 2) % len(gallery)].image
        floor.save()
    if floors:
        print(f"{prop.name}: floor_plan_image set on {len(floors)} floors")

print("Done.")
