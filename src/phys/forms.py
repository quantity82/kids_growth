from django import forms
from .models import PhysData
from users.models import KidsProfile
import bootstrap_datepicker_plus as datetimepicker


class PhysDataForm(forms.ModelForm):
    class Meta:
        model = PhysData
        fields = ('kidsProfile', 'weight', 'height', 'date',)
        widgets = {
            'date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(PhysDataForm, self).__init__(*args, **kwargs)
        self.fields['kidsProfile'] = forms.ModelChoiceField(queryset=KidsProfile.objects.filter(user=user))


class PhysDataEditForm(forms.ModelForm):
    class Meta:
        model = PhysData
        fields = ('weight', 'height', 'date',)
        widgets = {
            'date': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        kidsProfileId = kwargs.pop('kidsProfileId', '')
        super(PhysDataEditForm, self).__init__(*args, **kwargs)
