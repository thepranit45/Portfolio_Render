from django.core.management.base import BaseCommand
from portfolio.models import Project


class Command(BaseCommand):
    help = 'Create sample projects for the portfolio'
    
    def handle(self, *args, **options):
        # Clear existing projects
        Project.objects.all().delete()
        
        projects = [
            {
                'title': 'Student Result Management System',
                'short_description': 'A comprehensive result management system with admin dashboard, marks entry, and automatic CGPA calculation.',
                'description': '''A complete web-based result management system built for educational institutions. 
                
Features include:
- Admin dashboard for managing students and subjects
- Secure marks entry system with validation
- Automatic CGPA and percentage calculation
- Student result viewing and PDF download
- Role-based access control
- Responsive design for all devices''',
                'category': 'education',
                'status': 'completed',
                'technologies': 'PHP, MySQL, HTML5, CSS3, JavaScript, Bootstrap',
                'demo_url': 'https://your-demo-url.com',
                'github_url': 'https://github.com/thepranit45/student-result-system',
                'is_featured': True,
                'is_published': True,
                'display_order': 1
            },
            {
                'title': 'E-commerce Portfolio Website',
                'short_description': 'Modern portfolio website with integrated payment system and service management.',
                'description': '''A professional portfolio website with complete payment integration and service management capabilities.
                
Key features:
- Responsive design with modern UI/UX
- Razorpay payment integration
- Service management and booking
- Contact form with admin notifications
- SEO optimized and fast loading
- Mobile-first approach''',
                'category': 'web',
                'status': 'completed',
                'technologies': 'Django, Python, HTML5, CSS3, JavaScript, Razorpay API',
                'demo_url': 'https://portfo-d50i.onrender.com',
                'github_url': 'https://github.com/thepranit45/portfolio-website',
                'is_featured': True,
                'is_published': True,
                'display_order': 2
            }
        ]
        
        created_count = 0
        for project_data in projects:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created project: {project.title}')
                )
            else:
                # Update existing project
                for key, value in project_data.items():
                    setattr(project, key, value)
                project.save()
                self.stdout.write(
                    self.style.WARNING(f'Updated project: {project.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(projects)} projects!')
        )