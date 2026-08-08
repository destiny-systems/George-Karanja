from django.core.files import File
from portfolio.models import Property, LocationAdvantage

data = {
    "GK Luxurious Residence": {
        "image": "sample_images/location/westlands.jpg",
        "advantages": {
            "shopping": "Sarit Centre, Westgate Mall, The Oval, 9 West, ABC Place",
            "healthcare": "Aga Khan University Hospital, MP Shah Hospital, Nairobi Hospital",
            "education": "International School of Kenya (ISK), Peponi School, Braeburn School",
            "connectivity": "Nairobi CBD, United Nations Headquarters, Nairobi Expressway, Waiyaki Way",
        },
    },
    "Lewis Residence": {
        "image": "sample_images/location/nairobi_cbd.jpg",
        "advantages": {
            "shopping": "Yaya Centre, Junction Mall, Adlife Plaza",
            "healthcare": "Nairobi Hospital, Karen Hospital, MP Shah Hospital",
            "education": "Hillcrest International School, St Marys School, Nairobi Academy",
            "connectivity": "Ngong Road, Langata Road, Southern Bypass",
        },
    },
    "Cadillac Residence Kenya": {
        "image": "sample_images/location/nairobi_2.jpg",
        "advantages": {
            "shopping": "Two Rivers Mall, Village Market, Garden City Mall",
            "healthcare": "Gertrudes Children Hospital, Nairobi West Hospital",
            "education": "Braeside School, Rosslyn Academy, Kenton College",
            "connectivity": "Thika Superhighway, Kiambu Road, Nairobi Expressway",
        },
    },
}

for name, info in data.items():
    try:
        prop = Property.objects.get(name=name)
    except Property.DoesNotExist:
        print(f"SKIP: {name} not found")
        continue

    if not prop.location_image:
        with open(info["image"], "rb") as f:
            prop.location_image.save(info["image"].split("/")[-1], File(f), save=True)
        print(f"{name}: location_image set")

    for category, items in info["advantages"].items():
        adv, created = LocationAdvantage.objects.get_or_create(property=prop, category=category, defaults={"items": items})
        if created:
            print(f"  Added {category} advantage for {name}")

print("Done.")
