

from django import forms

# Email Form ####################
class EmailPostForm(forms.Form):
    subject    = forms.CharField(max_length=25)
    to      = forms.EmailField()
    message = forms.CharField(required=True, widget=forms.Textarea)
