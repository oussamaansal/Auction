from django import forms
from .models import *

  
class CloseAuctionForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm Close Auction", required=True)

class NewAucForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'start_bid', 'desc', 'categ', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categ': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {'required': 'Please enter a title.'},
            'start_bid': {'required': 'Please enter a valid starting bid.'},
            'desc': {'required': 'Please enter a description.'},
            'categ': {'required': 'Please select a category.'},
            'image_url': {'required': 'Please enter a valid image URL.'},
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your bid amount'
            })
        }