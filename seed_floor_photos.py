from portfolio.models import Property, Floor, UnitType

total_updated = 0
for prop in Property.objects.all():
    floors = Floor.objects.filter(property=prop)
    updated = 0
    for floor in floors:
        if floor.image or not floor.unit_type or not floor.unit_type.image:
            continue
        # Reuse the unit type's image as the floor's photo (same layout, different floor)
        floor.image = floor.unit_type.image
        floor.save()
        updated += 1
    print(f"{prop.name}: set images on {updated} floors")
    total_updated += updated

print(f"\nDone. Total floor images set: {total_updated}")
