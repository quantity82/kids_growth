from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import KidsProfile
import bootstrap_datepicker_plus as datetimepicker

User = get_user_model()

class SignUpForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class KidsProfileForm(forms.ModelForm):
    class Meta:
        model = KidsProfile
        fields = ('name', 'gender', 'birthday')
        widgets = {
            'birthday': datetimepicker.DatePickerInput(
                           format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(KidsProfileForm, self).__init__(*args, **kwargs)