from django import forms
from review.models import Review
from django.forms import HiddenInput

class RatingForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['taste', 'ambience', 'customer_service', 'value_for_money', 'location', 'comment_text']
        widgets = {
            'taste': HiddenInput(),              
            'ambience': HiddenInput(),           
            'location': HiddenInput(),          
            'customer_service': HiddenInput(),   
            'value_for_money': HiddenInput(),    
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment_text']
        


