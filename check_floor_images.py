from portfolio.models import Property, Floor, UnitType

for prop in Property.objects.all():
    print(f"=== {prop.name} ===")
    for u in UnitType.objects.filter(property=prop):
        print(f"  UnitType {u.name}: image={u.image or '(empty)'}")
    floors_with_img = Floor.objects.filter(property=prop, image__isnull=False).exclude(image='').count()
    floors_total = Floor.objects.filter(property=prop).count()
    print(f"  Floors with image set: {floors_with_img} / {floors_total}")
