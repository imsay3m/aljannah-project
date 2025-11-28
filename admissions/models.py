from django.db import models

class AdmissionCost(models.Model):
    """
    Stores fee structure: e.g. "Monthly Fee", "Registration Fee"
    """
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=50, help_text="e.g. £50 or 'Free'")
    description = models.TextField(blank=True, help_text="Extra details like 'per child'")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.amount}"


class ApplicationSubmission(models.Model):
    """
    Stores the online application form data.
    """
    # Student Details
    child_first_name = models.CharField(max_length=100)
    child_last_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    
    # Parent Details
    parent_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Meta
    notes = models.TextField(blank=True, help_text="Medical info or other notes")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.child_first_name} {self.child_last_name}"