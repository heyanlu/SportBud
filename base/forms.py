from django.forms import ModelForm, DateTimeInput
from django import forms
from .models import Activity, Review 

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'featured_image', 'description', 'scheduled_date', 'tags']
        
        widgets ={
            'tags': forms.CheckboxSelectMultiple(),
            'scheduled_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),

        }
        
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
        # self.fields['title'].widget.attrs.update({'class':'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review 
        fields = ['value', 'body']
        
    labels = {
        'value': 'Place your vote', 
        'body': 'Add a comment with your vote'
    }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})