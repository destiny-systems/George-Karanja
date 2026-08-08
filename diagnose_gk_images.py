from portfolio.models import Property, UnitType, GalleryImage, Floor

prop = Property.objects.get(name='GK Luxurious Residence')
print("hero_image:", prop.hero_image)
print("gallery count:", GalleryImage.objects.filter(property=prop).count())
for u in UnitType.objects.filter(property=prop):
    print(f"UnitType {u.name}: image={u.image or '(EMPTY)'}")
floors_with_img = Floor.objects.filter(property=prop, image__isnull=False).exclude(image='').count()
print(f"Floors with image: {floors_with_img} / {Floor.objects.filter(property=prop).count()}")
