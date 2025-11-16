from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','placeholder':'Your name'}),
            'email': forms.EmailInput(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','placeholder':'name@example.com'}),
            'message': forms.Textarea(attrs={'class':'w-full px-4 py-3 bg-dark border border-gray-700 rounded-lg','rows':5,'placeholder':'Your message'}),
        }
