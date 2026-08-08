import io
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from portfolio.models import Property


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))


class Command(BaseCommand):
    help = "Generate a colorful branded booklet PDF for every property"

    def handle(self, *args, **options):
        for prop in Property.objects.all():
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            accent_rgb = hex_to_rgb(prop.accent_color)
            accent = colors.Color(*accent_rgb)

            # ===== COVER PAGE =====
            c.setFillColor(colors.Color(0.07, 0.07, 0.07))
            c.rect(0, 0, width, height, fill=1, stroke=0)

            if prop.hero_image:
                try:
                    img = ImageReader(prop.hero_image.path)
                    c.drawImage(img, 0, height - 250*mm, width=width, height=250*mm,
                                preserveAspectRatio=True, anchor='n', mask='auto')
                except Exception:
                    pass

            c.setFillColor(accent)
            c.rect(0, height - 260*mm, width, 4*mm, fill=1, stroke=0)

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 34)
            c.drawString(20*mm, height - 290*mm, prop.name)

            c.setFont("Helvetica", 14)
            c.setFillColor(accent)
            c.drawString(20*mm, height - 300*mm, prop.location_name)

            c.setFont("Helvetica", 11)
            c.setFillColor(colors.Color(0.8, 0.8, 0.8))
            c.drawString(20*mm, height - 310*mm, prop.tagline[:90] if prop.tagline else "")

            c.showPage()

            # ===== ABOUT PAGE =====
            c.setFillColor(colors.white)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 22)
            c.drawString(20*mm, height - 30*mm, "About This Development")

            c.setFillColor(colors.Color(0.2, 0.2, 0.2))
            c.setFont("Helvetica", 11)
            text = c.beginText(20*mm, height - 45*mm)
            text.setLeading(16)
            about = prop.about_text or "A landmark residential development offering premium living spaces."
            words = about.split()
            line = ""
            for word in words:
                if len(line + " " + word) > 90:
                    text.textLine(line)
                    line = word
                else:
                    line = (line + " " + word).strip()
            if line:
                text.textLine(line)
            c.drawText(text)

            # Unit types table
            y = height - 100*mm
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(20*mm, y, "Unit Types & Pricing")
            y -= 12*mm

            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.white)
            c.setFillColor(accent)
            c.rect(20*mm, y - 4*mm, width - 40*mm, 8*mm, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.drawString(22*mm, y - 2*mm, "Unit Type")
            c.drawString(90*mm, y - 2*mm, "Size (sqm)")
            c.drawString(130*mm, y - 2*mm, "Price (KSh)")
            y -= 10*mm

            c.setFont("Helvetica", 10)
            for unit in prop.unit_types.all():
                c.setFillColor(colors.Color(0.15, 0.15, 0.15))
                c.drawString(22*mm, y - 2*mm, unit.name)
                c.drawString(90*mm, y - 2*mm, str(unit.size_sqm))
                c.drawString(130*mm, y - 2*mm, f"{unit.price:,.0f}")
                y -= 8*mm

            c.showPage()

            # ===== CONTACT PAGE =====
            c.setFillColor(colors.Color(0.07, 0.07, 0.07))
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width / 2, height / 2 + 20*mm, "Get In Touch")

            c.setFillColor(colors.white)
            c.setFont("Helvetica", 12)
            c.drawCentredString(width / 2, height / 2, "Minet House, 7th Floor, Nairobi, Kenya")
            c.drawCentredString(width / 2, height / 2 - 8*mm, "destinysystems00@gmail.com")
            c.drawCentredString(width / 2, height / 2 - 16*mm, "+254 702 432 722")

            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, height / 2 - 35*mm, "A George Karanja Development")

            c.showPage()
            c.save()

            buffer.seek(0)
            filename = f"{prop.slug}_booklet.pdf"
            prop.booklet_pdf.save(filename, ContentFile(buffer.read()), save=True)
            self.stdout.write(self.style.SUCCESS(f"Generated booklet for {prop.name}"))

        self.stdout.write(self.style.SUCCESS("\nAll booklets generated."))
