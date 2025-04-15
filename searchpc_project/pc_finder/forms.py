from django import forms

class PCSearchForm(forms.Form):
    PURPOSE_CHOICES = [
        ('Gaming', 'Gaming'),
        ('Programming', 'Programming'),
        ('Machine Learning', 'Machine Learning'),
        ('Video Editing', 'Video Editing'),
        ('General Use', 'General Use'),
        ('Professional Work', 'Professional Work'),
    ]
    
    BRAND_CHOICES = [
        ('Intel', 'Intel'),
        ('AMD', 'AMD'),
        ('NVIDIA', 'NVIDIA'),
        ('Samsung', 'Samsung'),
        ('Western Digital', 'Western Digital'),
    ]
    
    budget = forms.DecimalField(
        min_value=10000,
        max_value=1000000,
        initial=50000,
        label='Budget (INR)',
        widget=forms.NumberInput(attrs={'step': '5000'})
    )
    
    purpose = forms.ChoiceField(
        choices=PURPOSE_CHOICES,
        label='PC Purpose'
    )
    
    location = forms.CharField(
        max_length=100,
        label='Location',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Mumbai, India'})
    )
    
    preferred_brands = forms.MultipleChoiceField(
        choices=BRAND_CHOICES,
        label='Preferred Brands (Optional)',
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
