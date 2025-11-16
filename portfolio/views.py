from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import ContactForm
from .models import Contact
from django.http import Http404

def home(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact = form.save()
        # send email to DEFAULT_FROM_EMAIL (dev -> console)
        send_mail(
            subject=f"New contact from {contact.name}",
            message=contact.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        messages.success(request, "Thanks — your message was sent!")
        return redirect(reverse('portfolio:home') + '#contact')
    return render(request, 'portfolio/home.html', {'form': form})


def about(request):
    return render(request, 'portfolio/about.html')


def skills(request):
    return render(request, 'portfolio/skills.html')


def projects(request):
    return render(request, 'portfolio/projects.html')


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact = form.save()
        send_mail(
            subject=f"New contact from {contact.name}",
            message=contact.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        messages.success(request, "Thanks — your message was sent!")
        return redirect(reverse('portfolio:contact'))
    return render(request, 'portfolio/contact.html', {'form': form})


def project_student_result(request):
    """Project detail page for Student Result System (static page)."""
    # The template will contain Features, Technologies and Modules as requested
    return render(request, 'portfolio/project_student_result.html')


def project_detail(request, slug):
    """Generic project detail view. Looks up project data by slug and renders a detail page.

    We use a small in-memory map for content so we can render deep info pages without a DB.
    """
    projects = {
        'student-result': {
            'title': 'Student Result System',
            'short': 'Result management system with admin dashboard and automatic CGPA computation.',
            'features': [
                'Admin login & dashboard',
                'Add/manage students & subjects',
                'Enter marks and generate results',
                'Automatic CGPA, percentage & pass/fail calculation',
                'Students can view and download/print their results',
                'Secure and user-friendly interface',
            ],
            'technologies': {
                'frontend': 'HTML, CSS, JavaScript',
                'backend': 'PHP',
                'database': 'MySQL',
                'tools': 'XAMPP/WAMP, phpMyAdmin',
            },
            'modules': [
                'Admin Module: Manage students, subjects, marks, results',
                'Student Module: View & download result',
                'Result Module: CGPA, percentage, pass/fail processing',
            ],
        },
        # Add additional project slugs here as needed
    }

    project = projects.get(slug)
    if not project:
        raise Http404('Project not found')

    return render(request, 'portfolio/project_detail.html', {'project': project, 'slug': slug})
