from django.forms import ModelForm, Textarea
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating','price', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows': 5})
        }