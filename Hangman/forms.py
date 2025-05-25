from django import forms
from django.core.validators import RegexValidator
from Hangman.models import Try
class TryForm(forms.ModelForm):
    class Meta:
        model = Try
        fields = ["letter"]
        labels = {"letter": "Ваша буква"}
        widgets = {
            "letter": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введіть одну букву",
                    "maxlength": "1",
                    #"pattern": "[а-яА-Яa-zA-Z]",
                }
            )
        }
    def clean_letter(self):
        letter = self.cleaned_data["letter"]
        if not letter.isalpha():
            raise forms.ValidationError("Будь ласка, введіть одну букву з алфавіту.")
        return letter.lower()

