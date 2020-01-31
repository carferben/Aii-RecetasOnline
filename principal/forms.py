from django import forms

class CatForm(forms.Form):
    categorias = forms.CharField()