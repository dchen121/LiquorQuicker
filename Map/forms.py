from django.forms import ModelForm, Textarea, NumberInput
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating','price', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 20, 'rows': 10}),
            'price': NumberInput(attrs={'min': '-1', 'max': '105', 'step': '1',
            	})
        }