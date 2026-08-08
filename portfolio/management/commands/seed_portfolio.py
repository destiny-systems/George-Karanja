from django.core.management.base import BaseCommand
from portfolio.models import Property, UnitType, Floor


class Command(BaseCommand):
    def handle(self, *args, **options):
        properties_data = [
            {
                "name": "GK Luxurious Residence",
                "tagline": "Where luxury living and everyday amenities come together in Westlands.",
                "about_text": "GK Luxurious Residence stands as a beacon of modern luxury in Westlands, Nairobi, offering an unparalleled living experience. Our meticulously designed apartments combine contemporary architecture with premium finishes.",
                "card_summary": "Modern luxury apartments in the heart of Westlands.",
                "starting_price": 5000000,
                "location_name": "Westlands, Nairobi",
                "address": "Westlands, Nairobi, Kenya",
                "accent_color": "#c9a24b",
                "order": 1,
            },
            {
                "name": "Lewis Residence",
                "tagline": "An elite residential standard tailored around architectural elegance.",
                "about_text": "Lewis Residence is an elite, beautifully composed residential standard tailored flawlessly around architectural elegance and panoramic views, offering configurable layouts across a 14-floor tower.",
                "card_summary": "Configurable elite residences with panoramic views.",
                "starting_price": 5000000,
                "location_name": "Nairobi, Kenya",
                "address": "Nairobi, Kenya",
                "accent_color": "#ff6600",
                "order": 2,
            },
            {
                "name": "Cadillac Residence Kenya",
                "tagline": "Modern living, elevated design, unmatched comfort.",
                "about_text": "Cadillac Residence Kenya is a landmark development offering meticulously designed apartments across 20 floors of contemporary elegance, from cozy one-bedroom retreats to sprawling penthouses.",
                "card_summary": "Contemporary elegance across 20 floors of modern living.",
                "starting_price": 5000000,
                "location_name": "Nairobi, Kenya",
                "address": "Nairobi, Kenya",
                "accent_color": "#d4a13d",
                "order": 3,
            },
        ]

        for pdata in properties_data:
            prop, created = Property.objects.get_or_create(name=pdata["name"], defaults=pdata)
            status = "Created" if created else "Already exists"
            self.stdout.write(self.style.SUCCESS(f"{status}: {prop.name}"))

            units = [
                ("One Bedroom", 1, 50.0, 5000000, "A cozy, efficient layout for modern living."),
                ("Two Bedroom", 2, 85.0, 8500000, "Spacious family living with premium finishes."),
                ("Penthouse", 4, 220.0, 12000000, "The pinnacle of luxury with panoramic views."),
            ]
            unit_objs = {}
            for name, beds, size, price, desc in units:
                u, _ = UnitType.objects.get_or_create(
                    property=prop, name=name,
                    defaults=dict(bedrooms=beds, size_sqm=size, price=price, description=desc)
                )
                unit_objs[name] = u

            cycle = [("One Bedroom", 5000000), ("Two Bedroom", 8500000), ("Penthouse", 12000000)]
            Floor.objects.filter(property=prop).delete()
            for i in range(1, 21):
                uname, price = cycle[(i - 1) % 3]
                floor_label = "Penthouse Suite" if i == 20 else f"Unit {i}{uname[0]}"
                Floor.objects.create(
                    property=prop, unit_type=unit_objs[uname],
                    floor_number="Penthouse Floor" if i == 20 else f"Floor {i}",
                    unit_label=f"{floor_label} - {uname}", price=price, order=i,
                )

            self.stdout.write(f"  -> {UnitType.objects.filter(property=prop).count()} unit types, {Floor.objects.filter(property=prop).count()} floors")

        self.stdout.write(self.style.SUCCESS("\nDone. All 3 properties seeded."))
