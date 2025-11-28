from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class Policy(models.Model):
    """
    Stores 'Punctuality', 'Dress Code', 'Data Protection', etc.
    """
    title = models.CharField(max_length=200)
    content = CKEditor5Field("Policy Content", config_name="extends")
    order = models.IntegerField(default=0, help_text="Order in which to display the policy")

    class Meta:
        verbose_name_plural = "Policies"
        ordering = ['order']

    def __str__(self):
        return self.title


class DailySchedule(models.Model):
    """
    Stores the time plan: 11:00 Islamic Studies, 12:50 Lunch, etc.
    """

    # CHANGED: Both fields are now optional (null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True, help_text="Optional end time")

    activity = models.CharField(
        max_length=200, help_text="e.g. 'Islamic Studies' or 'Registration'"
    )
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Class Schedule Item"
        ordering = ["order", "start_time"]

    def __str__(self):
        # Handle display string if time is missing
        time_str = self.start_time.strftime("%H:%M") if self.start_time else "No Time"
        return f"{time_str} - {self.activity}"


class Level(models.Model):
    """
    Academic Levels (e.g. Level 1, Level 2, Foundation)
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Books published by the Academy
    """

    # CHANGED: Renamed field from 'subject' to 'level'
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="books")

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, default="Al Jannah Academy")
    cover_image = models.ImageField(upload_to="books/covers/", blank=True, null=True)

    # Optional free download link
    pdf_file = models.FileField(
        upload_to="books/pdfs/",
        blank=True,
        null=True,
        help_text="Optional free download link",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price in £ (e.g. 17.00)",
    )

    def __str__(self):
        return self.title


class PurchaseLink(models.Model):
    """
    Stores links to Amazon, eBay, etc. for a specific book.
    """

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="purchase_links"
    )
    vendor_name = models.CharField(
        max_length=50, help_text="e.g. Amazon, Waterstones, eBay"
    )
    url = models.URLField(help_text="Paste the full link here")

    def __str__(self):
        return f"{self.vendor_name} link for {self.book.title}"


class BookOrder(models.Model):
    CLASS_CHOICES = [
        ("K", "Kindergarten (K)"),
        ("1", "Class 1"),
        ("2", "Class 2"),
        ("3", "Class 3"),
        ("4", "Class 4"),
        ("5", "Class 5"),
        ("6", "Class 6"),
        ("7", "Class 7"),
    ]

    REASON_CHOICES = [
        ("new", "New student"),
        ("promoted", "Promoted"),
        ("missing", "Missing"),
        ("other", "Other"),
    ]

    student_name = models.CharField(max_length=200, verbose_name="Student Full Name")
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    parent_name = models.CharField(max_length=200, verbose_name="Parent Full Name")
    parent_mobile = models.CharField(max_length=20)
    parent_email = models.EmailField()

    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    other_reason_details = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="If other, please specify"
    )

    selected_books = models.TextField(
        blank=True,
        null=True,
        help_text="List of books selected by the user (if Reason is Missing)",
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.student_name} ({self.student_class})"
