from django.core.management.base import BaseCommand
from portfolio.models import Service


class Command(BaseCommand):
    help = 'Create sample services for testing the payment system'

    def handle(self, *args, **options):
        # Clear existing services
        Service.objects.all().delete()
        
        services = [
            {
                'name': 'Code Review Service',
                'description': 'Professional code review with detailed feedback on code quality, performance, security vulnerabilities, and best practices. Includes written report with actionable recommendations.',
                'service_type': 'consultation',
                'price': 10.00,
                'duration': '2-3 hours',
                'is_active': True
            },
            {
                'name': 'IoT Project Development',
                'description': 'Complete IoT solution with sensor integration, basic data collection, cloud connectivity (Firebase/AWS), and simple monitoring dashboard. Custom sensors and advanced features quoted separately.',
                'service_type': 'development',
                'price': 15000.00,
                'duration': '3-4 weeks',
                'is_active': True
            },
            {
                'name': 'Android Development',
                'description': 'Native Android app with modern UI/UX (up to 5 screens), basic API integration, local database, and Google Play Store submission. Advanced features and complex integrations quoted separately.',
                'service_type': 'development',
                'price': 12000.00,
                'duration': '3-5 weeks',
                'is_active': True
            },
            {
                'name': 'Automation Solutions',
                'description': 'Custom automation script for business processes including web scraping (up to 3 sites), basic workflow automation, or simple task scheduling. Complex enterprise solutions quoted separately.',
                'service_type': 'development',
                'price': 8000.00,
                'duration': '2-3 weeks',
                'is_active': True
            }
        ]
        
        created_count = 0
        for service_data in services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} services!')
        )