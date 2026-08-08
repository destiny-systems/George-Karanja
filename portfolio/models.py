from django.db import models
from django.urls import reverse


class Property(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    about_text = models.TextField(blank=True)
    card_summary = models.CharField(max_length=250, blank=True, help_text="Short blurb for the homepage card")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_video = models.FileField(upload_to='hero/', blank=True, null=True)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, default=5000000)
    location_name = models.CharField(max_length=150, default="Nairobi, Kenya")
    address = models.CharField(max_length=200, blank=True)
    accent_color = models.CharField(max_length=20, default="#c9a24b", help_text="Hex color, e.g. #c9a24b (gold) or #ff6600 (orange)")
    location_image = models.ImageField(upload_to='location/', blank=True, null=True, help_text="Photo representing the neighbourhood")
    booklet_pdf = models.FileField(upload_to='booklets/', blank=True, null=True, help_text="Downloadable brochure PDF")
    construction_percent = models.PositiveSmallIntegerField(default=60, help_text="Construction completion percentage")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'slug': self.slug})


class UnitType(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='unit_types')
    name = models.CharField(max_length=100)
    bedrooms = models.PositiveSmallIntegerField(default=1)
    size_sqm = models.DecimalField(max_digits=6, decimal_places=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=250, blank=True)
    features = models.TextField(blank=True)
    image = models.ImageField(upload_to='unit_types/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'bedrooms']

    def __str__(self):
        return f"{self.property.name} - {self.name}"

    def features_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class RoomImage(models.Model):
    ROOM_TYPE_CHOICES = [
        ('living_room', 'Living Room'), ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'), ('bathroom', 'Bathroom'),
    ]
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, related_name='room_images')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    image = models.ImageField(upload_to='room_images/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['room_type', 'order']

    def __str__(self):
        return f"{self.unit_type} - {self.get_room_type_display()}"


class Floor(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='floors')
    unit_type = models.ForeignKey(UnitType, on_delete=models.SET_NULL, blank=True, null=True, related_name='floors')
    floor_number = models.CharField(max_length=20)
    unit_label = models.CharField(max_length=100)
    image = models.ImageField(upload_to='floors/', blank=True, null=True)
    floor_plan_image = models.ImageField(upload_to='floor_plans/', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.property.name} - {self.floor_number} - {self.unit_label}"


class GalleryImage(models.Model):
    ROOM_TYPE_CHOICES = [
        ('living_room', 'Living Room'), ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'), ('bathroom', 'Bathroom'), ('construction', 'Construction Progress'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery_images')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or f"Gallery #{self.pk}"


class Enquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='enquiries')
    unit_type = models.ForeignKey(UnitType, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.full_name} - {self.property.name}"


class Payment(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=200, blank=True)
    customer_email = models.EmailField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default="usd")
    status = models.CharField(max_length=30, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.stripe_session_id} - {self.status}"


class LocationAdvantage(models.Model):
    CATEGORY_CHOICES = [
        ('shopping', 'Shopping & Entertainment'),
        ('healthcare', 'Healthcare Facilities'),
        ('education', 'Educational Institutions'),
        ('connectivity', 'Connectivity & Access'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='location_advantages')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    items = models.TextField(help_text="Comma-separated list, e.g. Sarit Centre, Westgate Mall")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.property.name} - {self.get_category_display()}"

    def items_list(self):
        return [i.strip() for i in self.items.split(',') if i.strip()]


class PortfolioOwner(models.Model):
    """Singleton for George Karanja's own info/photo shown on the portfolio homepage."""
    name = models.CharField(max_length=120, default="George Karanja")
    photo = models.ImageField(upload_to='owner/', blank=True, null=True)
    bio = models.TextField(blank=True)
    homepage_background = models.ImageField(upload_to='owner/', blank=True, null=True, help_text="Animated background photo for the portfolio homepage")

    def __str__(self):
        return self.name
