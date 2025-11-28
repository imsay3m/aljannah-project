from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Project(models.Model):
    """
    Handles: Al Naseer Foundation, WhatsApp Groups, Counselling, Skype Sessions
    """

    title = models.CharField(max_length=200)
    description = CKEditor5Field("Description", config_name="extends")
    # Dynamic Contact info (some projects might have specific contacts different from Headteacher)
    contact_person = models.CharField(
        max_length=100, blank=True, help_text="e.g. Sister Nazish"
    )
    contact_number = models.CharField(
        max_length=50, blank=True, help_text="e.g. 07783..."
    )

    # External Links (e.g. for Fee structure or Counselling website)
    external_link = models.URLField(
        blank=True, help_text="Link to external site or fee PDF"
    )
    link_text = models.CharField(
        max_length=50, default="Click here for details", help_text="Text for the button"
    )

    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
