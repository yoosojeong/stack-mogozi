from django import forms

from .models import *


class UserJoinForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('id', 'password', 'gender', 'email')

class ChangeWordForm(forms.ModelForm):
    class Meta:
        model = ChangeWordModel
        fields = ('id', 'original_sentence',)