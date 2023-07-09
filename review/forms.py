from django import forms
from review.models import Review


class RatingForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['taste', 'ambience', 'customer_service', 'value_for_money', 'location', 'comment_text']

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment_text']
        


