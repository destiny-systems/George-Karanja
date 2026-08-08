import os
from django.core.files import File
from portfolio.models import Property, UnitType, RoomImage

folder_property_map = {
    'sample_images/gk': 'GK Luxurious Residence',
    'sample_images/lewis': 'Lewis Residence',
    'sample_images/gallery': 'Cadillac Residence Kenya',
}

room_types = ['living_room', 'kitchen', 'bedroom', 'bathroom']
prefix_map = {'living_room': 'living', 'kitchen': 'kitchen', 'bedroom': 'bedroom', 'bathroom': 'bathroom'}

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

    files = sorted(os.listdir(folder))
    unit_types = list(UnitType.objects.filter(property=prop))
    if not unit_types:
        print(f"SKIP: no UnitType records for {property_name}")
        continue

    # Set the unit type's main image from the living room photo (index 1) if not already set
    for i, unit in enumerate(unit_types):
        candidate = next((f for f in files if f.startswith('living_')), None)
        if candidate and not unit.image:
            filepath = os.path.join(folder, candidate)
            with open(filepath, 'rb') as f:
                unit.image.save(f"{unit.name}_{candidate}", File(f), save=True)
            print(f"  Set main image for {property_name} - {unit.name}")

    # Assign one room image per room_type per unit type, cycling through the 5 available per category
    created = 0
    for unit in unit_types:
        for room_type in room_types:
            if RoomImage.objects.filter(unit_type=unit, room_type=room_type).exists():
                continue
            prefix = prefix_map[room_type]
            candidates = [f for f in files if f.startswith(prefix + '_')]
            if not candidates:
                continue
            filename = candidates[hash(unit.name) % len(candidates)]
            filepath = os.path.join(folder, filename)
            with open(filepath, 'rb') as f:
                ri = RoomImage(unit_type=unit, room_type=room_type)
                ri.image.save(f"{unit.name}_{filename}", File(f), save=True)
            created += 1

    print(f"{property_name}: added {created} room images across {len(unit_types)} unit types")
    total_created += created

print(f"\nDone. Total room images added: {total_created}")
