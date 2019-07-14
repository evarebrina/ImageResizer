from django import forms


class ResizeForm(forms.Form):
    image = forms.ImageField()
    width = forms.IntegerField()
    height = forms.IntegerField()
