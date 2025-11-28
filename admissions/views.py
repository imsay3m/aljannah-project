from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdmissionCost
from .forms import ApplicationForm
from core.models import PageContent
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.models import SiteConfiguration


def admissions_overview(request):
    costs = AdmissionCost.objects.all()
    intro_content = PageContent.objects.filter(
        page="admissions", section_name="Intro"
    ).first()
    config = SiteConfiguration.objects.first()  # Get Site Config

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # 1. Save to Database
            application = form.save()

            # 2. Get Admin Email
            admin_email = config.email if config else "info@aljannahacademy.com"

            # 3. Prepare Email Data (Form cleaned_data matches template variables)
            context = form.cleaned_data

            # 4. Render HTML Template
            subject = f"New Admission Application: {application.child_first_name} {application.child_last_name}"
            html_content = render_to_string(
                "emails/admission_notification.html", context
            )
            text_content = strip_tags(html_content)

            # 5. Send Email
            try:
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email=None, to=[admin_email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(f"Email sending failed: {e}")

            messages.success(
                request,
                "Application submitted successfully! We will contact you shortly.",
            )
            return redirect("admissions")
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = ApplicationForm()

    context = {
        "costs": costs,
        "form": form,
        "intro_content": intro_content,
        "site_config": config,  # Pass config for the toggle logic
    }
    return render(request, "admissions/admissions.html", context)
