from django import forms

# search form


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search CS50 Wiki"}))


class CreateForm(forms.Form):
    """ Form Class for Creating New Entries """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "placeholder": "Page Title"}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Github Markdown"
    }))


class EditForm(forms.Form):
    """ Form Class for Editing Entries """
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Github Markdown"
    }))
