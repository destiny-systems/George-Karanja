import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as flash
from django.urls import reverse
from .models import Property, Floor, PortfolioOwner
from .forms import EnquiryForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def portfolio_home(request):
    properties = Property.objects.all()
    owner = PortfolioOwner.objects.first()
    return render(request, "portfolio/home.html", {"properties": properties, "owner": owner})


def property_detail(request, slug):
    prop = get_object_or_404(Property, slug=slug)

    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.property = prop
            enquiry.save()
            flash.success(request, "Thank you! Our team will reach out shortly.")
            return redirect("property_detail", slug=slug)
    else:
        form = EnquiryForm()

    form.fields["unit_type"].queryset = prop.unit_types.all()

    context = {
        "property": prop,
        "unit_types": prop.unit_types.prefetch_related("room_images").all(),
        "gallery_images": prop.gallery_images.all(),
        "floors": prop.floors.all(),
        "location_advantages": prop.location_advantages.all(),
        "form": form,
    }
    return render(request, "portfolio/property_detail.html", context)


def create_checkout_session(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    if not floor.price:
        flash.error(request, "This unit is not available for payment right now.")
        return redirect("property_detail", slug=floor.property.slug)

    amount_cents = int(floor.price * 100)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": settings.STRIPE_CURRENCY,
                "product_data": {"name": f"{floor.property.name} - {floor.unit_label} - {floor.floor_number}"},
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
    )
    return redirect(checkout_session.url, permanent=False)


def payment_success(request):
    return render(request, "portfolio/payment_success.html")


def payment_cancel(request):
    return render(request, "portfolio/payment_cancel.html")
