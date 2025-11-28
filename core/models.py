from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import re

class SiteConfiguration(models.Model):
    """
    Singleton model to store global site settings.
    Only one instance of this should exist.
    """

    site_name = models.CharField(max_length=200, default="Al Jannah Academy")
    tagline = models.CharField(
        max_length=255, default="A structured and well equipped academy..."
    )
    head_teacher_name = models.CharField(
        max_length=100, default="Nazish Naseer", verbose_name="Head Teacher Name"
    )
    head_teacher_phone = models.CharField(
        max_length=50, default="07783 469546", verbose_name="Head Teacher Phone"
    )
    email = models.EmailField(
        default="aljannahacademy@gmail.com", verbose_name="Head Teacher / Main Email"
    )
    admin_contact_name = models.CharField(
        max_length=100, default="M Hanif Islam", verbose_name="Admissions Name"
    )
    admin_contact_phone = models.CharField(
        max_length=50, default="07985 786786", verbose_name="Admissions Phone"
    )
    admin_contact_email = models.EmailField(
        blank=True,
        default="hislam.aljannahacademy@gmail.com",
        verbose_name="Admissions Email",
    )
    address = models.TextField(default="Royal Lane, Uxbridge, UB8 3RF")
    use_external_admission_form = models.BooleanField(
        default=False,
        verbose_name="Use Third-Party Link?",
        help_text="Check this to hide the built-in form and show a 'Register Now' button pointing to an external site.",
    )

    # CHANGED: From TextField to URLField
    external_admission_url = models.URLField(
        blank=True,
        verbose_name="Third-Party Registration URL",
        help_text="Paste the full link here (e.g., https://app.joinin.online/...)",
    )

    # Social / External
    google_maps_embed = models.TextField(
        blank=True, help_text="Paste the iframe code here"
    )
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    x_link = models.URLField(blank=True, verbose_name="X (Twitter) Link")
    linkedin_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True, verbose_name="YouTube Link")
    whatsapp_link = models.URLField(blank=True)

    calendar_sidebar_image = models.ImageField(
        upload_to="site_assets/",
        blank=True,
        null=True,
        help_text="Upload a vertical portrait image to show on the right side of the calendar page.",
    )

    # Footer Timings
    term_timings = models.CharField(
        max_length=200, default="Saturdays: 11:00 AM - 2:00 PM (Term Time Only)"
    )
    facebook_embed_code = models.TextField(
        blank=True,
        verbose_name="Facebook Page Plugin Code",
        help_text="Go to https://developers.facebook.com/docs/plugins/page-plugin/, generate the IFrame code, and paste it here.",
    )

    featured_video_title = models.CharField(
        max_length=200,
        blank=True,
        default="About Al Jannah Academy",
        verbose_name="Featured Video Title",
    )

    featured_video_url = models.URLField(
        blank=True,
        verbose_name="YouTube Video Link",
        help_text="Paste the full YouTube URL (e.g., https://www.youtube.com/watch?v=...)",
    )
    @property
    def youtube_embed_url(self):
        """
        Converts standard YouTube link to Embed URL.
        """
        if not self.featured_video_url:
            return None

        # Regex to find video ID from various YouTube URL formats
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, self.featured_video_url)

        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return None

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"


class Service(models.Model):
    title = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional: FontAwesome icon class, e.g. 'fa-solid fa-book'",
    )

    # NEW FIELD
    image = models.ImageField(
        upload_to="services/",
        help_text="Upload an image (approx 400x300px)",
        blank=True,
        null=True,
    )

    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """
    Parents' feedback
    """

    parent_name = models.CharField(max_length=100)
    quote = models.TextField()
    child_info = models.CharField(
        max_length=100, blank=True, help_text="Optional: e.g. 'Mother of 2'"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.parent_name


class PageContent(models.Model):
    """
    Generic storage for About Us History, Welcome Message, etc.
    """

    PAGE_CHOICES = [
        ("home", "Home Page"),
        ("about", "About Us"),
        ("admissions", "Admissions"),
        ("syllabus", "Syllabus"),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES)
    section_name = models.CharField(
        max_length=100, help_text="e.g. 'History', 'Values', 'Admissions Intro'"
    )
    title = models.CharField(max_length=200, blank=True)
    content = CKEditor5Field("Content", config_name="extends")
    image = models.ImageField(upload_to="page_content/", blank=True, null=True)

    def __str__(self):
        return f"{self.get_page_display()} - {self.section_name}"


class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Headteacher")
    bio = CKEditor5Field("Bio", config_name="extends", blank=True)
    image = models.ImageField(upload_to="staff/", blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Staff Member"

    def __str__(self):
        return self.name


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name="Album Topic")
    cover_image = models.ImageField(upload_to="gallery/covers/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album = models.ForeignKey(
        GalleryAlbum, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="gallery/photos/")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image in {self.album.title}"


class ContactSubmission(models.Model):
    """
    Stores 'Contact Us' form data in the database.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(
        max_length=50,
        choices=[
            ("general", "General Enquiries"),
            ("admissions", "Admissions"),
            ("safeguarding", "Safeguarding"),
            ("volunteering", "Volunteering"),
        ],
    )
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"
