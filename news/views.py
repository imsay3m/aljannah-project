from django.shortcuts import render, get_object_or_404
from .models import NewsPost, Event
from django.utils import timezone

def news_list(request):
    posts = NewsPost.objects.filter(is_published=True, date__lte=timezone.now()).order_by("-date")
    return render(request, "news/news_list.html", {"posts": posts})

def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug)
    return render(request, "news/news_detail.html", {"post": post})

def calendar_view(request):
    # Show upcoming events first
    events = Event.objects.filter(date__gte=timezone.now()).order_by("date")
    return render(request, "news/calendar.html", {"events": events})