from django import forms
from review.models import Reviews, Comment


class RatingForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['taste', 'ambience', 'customer_service', 'value_for_money', 'location']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        


