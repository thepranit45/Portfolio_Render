from django import forms
from .models import Contact, PaymentOrder, Service


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','placeholder':'Your name'}),
            'email': forms.EmailInput(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','placeholder':'name@example.com'}),
            'message': forms.Textarea(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','rows':5,'placeholder':'Your message'}),
        }


class PaymentForm(forms.ModelForm):
    """Form for creating payment orders"""
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label="Select a service",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    class Meta:
        model = PaymentOrder
        fields = ['customer_name', 'customer_email', 'customer_phone', 'description']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Your full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'your@email.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': '+91 9970343404'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'Additional requirements or notes...'
            }),
        }
        labels = {
            'customer_name': 'Full Name',
            'customer_email': 'Email Address',
            'customer_phone': 'Phone Number',
            'description': 'Additional Notes',
        }

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if phone:
            # Remove any non-digit characters for validation
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 10:
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class ServiceForm(forms.ModelForm):
    """Form for creating/editing services (admin use)"""
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg',
                'placeholder': 'Service name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg',
                'rows': 4
            }),
            'service_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg',
                'step': '0.01'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg',
                'placeholder': 'e.g., 1 hour, 1 week, etc.'
            }),
        }
