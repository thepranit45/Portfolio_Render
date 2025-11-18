from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('projects/student-result/', views.project_student_result, name='project_student_result'),
    path('projects/attendance-management/', views.project_attendance_management, name='project_attendance_management'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    
    # Policy Pages
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('refund/', views.refund, name='refund'),
    path('delivery/', views.delivery, name='delivery'),
    
    # Payment URLs (Disabled - Using WhatsApp purchasing)
    path('services/', views.services, name='services'),
    # path('payment/create/<int:service_id>/', views.create_payment, name='create_payment'),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    # path('payment/success/<str:order_id>/', views.payment_success, name='payment_success'),
    # path('payment/failure/', views.payment_failure, name='payment_failure'),
    # path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
]
