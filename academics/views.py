from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Level, Policy, DailySchedule
from .forms import BookOrderForm
from core.models import PageContent, SiteConfiguration


def syllabus_view(request):
    """
    Displays Levels, Books, and handles Book Order Form.
    """
    levels = Level.objects.prefetch_related("books").all()
    intro_content = PageContent.objects.filter(
        page="syllabus", section_name="Intro"
    ).first()

    if request.method == "POST":
        form = BookOrderForm(request.POST)
        if form.is_valid():
            # 1. Save to DB
            order = form.save()

            # 2. Determine Recipient (Dynamic)
            config = SiteConfiguration.objects.first()

            if config and config.admin_contact_email:
                recipient = config.admin_contact_email
            else:
                recipient = "hislam.aljannahacademy@gmail.com"

            # 3. Send Email
            subject = f"Book Order: {order.student_name} (Class {order.student_class})"

            context = {
                "student_name": order.student_name,
                "student_class": order.get_student_class_display(),
                "parent_name": order.parent_name,
                "parent_mobile": order.parent_mobile,
                "parent_email": order.parent_email,
                "reason": order.get_reason_display(),
                "other_reason_details": order.other_reason_details,
                "selected_books": order.selected_books,  # ADDED THIS
            }

            html_content = render_to_string(
                "emails/book_order_notification.html", context
            )
            text_content = strip_tags(html_content)

            try:
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email=None, to=[recipient]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(
                    request,
                    "Order submitted! We will contact you shortly regarding collection.",
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.warning(
                    request,
                    "Order saved, but email notification failed. We will check the system.",
                )

            return redirect("syllabus")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookOrderForm()

    return render(
        request,
        "academics/syllabus.html",
        {
            "levels": levels,
            "intro_content": intro_content,
            "form": form,  # Pass form to template
        },
    )


def policies_view(request):
    policies = Policy.objects.all()
    schedule = DailySchedule.objects.all()
    intro = PageContent.objects.filter(section_name='Policies Intro').first()

    return render(request, "academics/policies.html", {
        "policies": policies,
        "schedule": schedule,
        "intro": intro
    })
