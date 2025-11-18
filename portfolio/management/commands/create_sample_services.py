from django.core.management.base import BaseCommand
from portfolio.models import Service


class Command(BaseCommand):
    help = 'Create sample services for testing the payment system'

    def handle(self, *args, **options):
        # Clear existing services
        Service.objects.all().delete()
        
        services = [
            {
                'name': 'Technical Consultation',
                'description': 'One-on-one technical consultation session to discuss your project requirements, technology stack, architecture decisions, and best practices.',
                'service_type': 'consultation',
                'price': 2500.00,
                'duration': '1 hour',
                'is_active': True
            },
            {
                'name': 'Website Development',
                'description': 'Complete responsive website development using modern technologies like React, Django, or Next.js with custom design and functionality.',
                'service_type': 'development',
                'price': 15000.00,
                'duration': '2-3 weeks',
                'is_active': True
            },
            {
                'name': 'Mobile App Development',
                'description': 'Native or cross-platform mobile app development for Android and iOS with modern UI/UX and backend integration.',
                'service_type': 'development',
                'price': 25000.00,
                'duration': '4-6 weeks',
                'is_active': True
            },
            {
                'name': 'Website Maintenance',
                'description': 'Monthly website maintenance including updates, security patches, performance optimization, and technical support.',
                'service_type': 'maintenance',
                'price': 3000.00,
                'duration': '1 month',
                'is_active': True
            },
            {
                'name': 'Python Training',
                'description': 'Comprehensive Python programming training covering basics to advanced topics including Django, data structures, and web development.',
                'service_type': 'training',
                'price': 8000.00,
                'duration': '10 sessions',
                'is_active': True
            },
            {
                'name': 'React.js Workshop',
                'description': 'Hands-on React.js workshop covering components, hooks, state management, and modern development practices with real projects.',
                'service_type': 'training',
                'price': 6000.00,
                'duration': '8 sessions',
                'is_active': True
            },
            {
                'name': 'Code Review Service',
                'description': 'Professional code review with detailed feedback on code quality, performance, security, and best practices recommendations.',
                'service_type': 'consultation',
                'price': 1500.00,
                'duration': '2-3 hours',
                'is_active': True
            },
            {
                'name': 'Custom E-commerce Solution',
                'description': 'Complete e-commerce platform development with payment integration, inventory management, and admin dashboard.',
                'service_type': 'development',
                'price': 35000.00,
                'duration': '6-8 weeks',
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