Live Website - https://portfo-d50i.onrender.com/ 




Pranit Gopale — Portfolio Website
A personal portfolio and product listing site built with Django. The site showcases projects (Student Result System, Attendance Management System), provides downloadable documentation PDFs, and uses WhatsApp as the primary contact / purchase channel.

Live preview: (self-hosted / see deployment)

Features
Landing / home page with hero, CTAs, and social links
Project listing and project detail pages
Downloadable PDF documentation for projects (in static/portfolio/documents/)
WhatsApp-based purchase/contact flow (no payment gateway integrated)
Responsive layout with Tailwind CSS and custom animations (GSAP, particle background)
Small interactive UI touches: custom cursor, floating tech elements, polished header
PostgreSQL-ready configuration
Admin interface for managing projects (Django admin)
Notable projects included:

Student Result System (result management, CGPA calculation, downloads)
Attendance Management System (analytics, automated reporting)
Tech stack
Python 3.11+ (project uses standard Django)
Django 4.x
PostgreSQL (recommended for production)
Tailwind CSS (via CDN)
GSAP (animations)
Three.js (importmap for optional 3D / three examples)
Vanilla JavaScript for UI interactions (in main.js)
Project structure highlights:

manage.py — Django CLI
portfolio — Django app (templates, models, views)
portfolio — all front-end templates (home, projects, project_detail, etc.)
portfolio — CSS, JS, images, PDF docs
requirements.txt — Python dependencies

