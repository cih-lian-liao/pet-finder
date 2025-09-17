from django import forms
from django.core.validators import RegexValidator


class PetSearchForm(forms.Form):
    """
    Form for searching pets on PetFinder.
    
    This form validates user input for pet search parameters
    including location and animal type.
    """
    
    # City validation - only letters, spaces, hyphens, and apostrophes
    city_validator = RegexValidator(
        regex=r'^[a-zA-Z\s\-\']+$',
        message='City name can only contain letters, spaces, hyphens, and apostrophes.'
    )
    
    # State validation - only letters, spaces, hyphens
    state_validator = RegexValidator(
        regex=r'^[a-zA-Z\s\-]+$',
        message='State name can only contain letters, spaces, and hyphens.'
    )
    
    city = forms.CharField(
        max_length=100,
        required=True,
        validators=[city_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city name (e.g., Seattle)',
            'id': 'city'
        }),
        help_text='Enter the city where you want to search for pets.'
    )
    
    state = forms.ChoiceField(
        choices=[
            ('', 'Select State'),
            ('AL', 'Alabama'),
            ('AK', 'Alaska'),
            ('AZ', 'Arizona'),
            ('AR', 'Arkansas'),
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            ('DE', 'Delaware'),
            ('DC', 'District of Columbia'),
            ('FL', 'Florida'),
            ('GA', 'Georgia'),
            ('HI', 'Hawaii'),
            ('ID', 'Idaho'),
            ('IL', 'Illinois'),
            ('IN', 'Indiana'),
            ('IA', 'Iowa'),
            ('KS', 'Kansas'),
            ('KY', 'Kentucky'),
            ('LA', 'Louisiana'),
            ('ME', 'Maine'),
            ('MD', 'Maryland'),
            ('MA', 'Massachusetts'),
            ('MI', 'Michigan'),
            ('MN', 'Minnesota'),
            ('MS', 'Mississippi'),
            ('MO', 'Missouri'),
            ('MT', 'Montana'),
            ('NE', 'Nebraska'),
            ('NV', 'Nevada'),
            ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'),
            ('NY', 'New York'),
            ('NC', 'North Carolina'),
            ('ND', 'North Dakota'),
            ('OH', 'Ohio'),
            ('OK', 'Oklahoma'),
            ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),
            ('TX', 'Texas'),
            ('UT', 'Utah'),
            ('VT', 'Vermont'),
            ('VA', 'Virginia'),
            ('WA', 'Washington'),
            ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'),
            ('WY', 'Wyoming'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'state'
        }),
        help_text='Select the state where you want to search for pets.'
    )
    
    animal = forms.ChoiceField(
        choices=[
            ('', 'Select Animal Type'),
            ('dog', '🐕 Dogs'),
            ('cat', '🐱 Cats'),
            ('bird', '🐦 Birds'),
            ('rabbit', '🐰 Rabbits'),
            ('small-furry', '🐹 Small & Furry'),
            ('horse', '🐴 Horses'),
            ('barnyard', '🐷 Barnyard Animals'),
            ('reptile', '🦎 Reptiles'),
            ('amphibian', '🐸 Amphibians'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'animal'
        }),
        help_text='Select the type of animal you want to find.'
    )
    
    distance = forms.ChoiceField(
        choices=[
            (10, '🔍 10 miles (Very Local)'),
            (30, '📍 30 miles (Local Area)'),
            (50, '🗺️ 50 miles (Wider Region)'),
            (100, '🌎 100 miles (Extended Area)'),
            (200, '🚗 200 miles (Road Trip)'),
            (500, '✈️ 500 miles (Willing to Travel)'),
        ],
        required=True,
        initial=100,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'distance'
        }),
        help_text='Select your preferred search radius.'
    )
    
    
    def clean_city(self):
        """Clean and normalize city input."""
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise forms.ValidationError('City is required.')
        return city.title()
    
    def clean_state(self):
        """Clean and validate state selection."""
        state = self.cleaned_data.get('state', '').strip()
        if not state:
            raise forms.ValidationError('Please select a state.')
        return state.upper()
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        
        # Additional validation could be added here
        # For example, checking if the combination of city/state is valid
        
        return cleaned_data


class PetFilterForm(forms.Form):
    """
    Form for filtering displayed pets.
    """
    
    breed = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by breed'
        })
    )
    
    sex = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    size = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
            ('extra_large', 'Extra Large'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    age = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('baby', 'Baby'),
            ('young', 'Young'),
            ('adult', 'Adult'),
            ('senior', 'Senior'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
