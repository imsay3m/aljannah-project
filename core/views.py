from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
    Service,
    Testimonial,
    StaffMember,
    GalleryAlbum,
    PageContent,
    SiteConfiguration,
)
from .forms import ContactForm
from news.models import NewsPost, Event
from academics.models import Book
from news.models import Announcement
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(request):
    """
    Homepage: Loads Services, Testimonials, Latest News, Upcoming Events.
    """
    context = {
        "announcements": Announcement.objects.filter(is_active=True).order_by(
            "-created_at"
        ),
        "services": Service.objects.all(),
        "testimonials": Testimonial.objects.filter(is_active=True),
        "latest_news": NewsPost.objects.filter(is_published=True)[:3],
        "upcoming_events": Event.objects.order_by("date")[:3],
        # Fetching specific Home Page content blocks (Welcome message, etc)
        "welcome_content": PageContent.objects.filter(
            page="home", section_name="Welcome"
        ).first(),
    }
    return render(request, "index.html", context)


def about_us(request):
    """
    About Page: Loads History, Values, and Staff.
    """
    context = {
        "history": PageContent.objects.filter(
            page="about", section_name="History"
        ).first(),
        "values": PageContent.objects.filter(
            page="about", section_name="Values"
        ).first(),
        "staff": StaffMember.objects.all(),
    }
    return render(request, "about.html", context)


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # 1. Save to Database
            submission = form.save()

            # 2. Get Admin Email from Site Configuration
            config = SiteConfiguration.objects.first()
            admin_email = config.email if config else "info@aljannahacademy.com"

            # 3. Prepare Email Data
            subject = (
                f"New Inquiry: {submission.subject.title()} from {submission.name}"
            )
            context = {
                "name": submission.name,
                "email": submission.email,
                "phone": submission.phone,
                "subject": submission.subject,
                "message": submission.message,
            }

            # 4. Render HTML Template
            html_content = render_to_string("emails/contact_notification.html", context)
            text_content = strip_tags(
                html_content
            )  # Fallback for text-only email clients

            # 5. Send Email
            try:
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email=None, to=[admin_email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log error but don't crash site

            messages.success(
                request, "Thank you! Your message has been sent to Al Jannah Academy."
            )
            return redirect("contact_us")
    else:
        form = ContactForm()

    return render(request, "contact_us.html", {"form": form})


def gallery(request):
    albums = GalleryAlbum.objects.all().order_by("-created_at")
    return render(request, "gallery.html", {"albums": albums})


def gallery_detail(request, pk):
    album = get_object_or_404(GalleryAlbum, pk=pk)
    return render(request, "gallery_detail.html", {"album": album})
