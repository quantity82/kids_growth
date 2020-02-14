from django import forms
from .models import ShoesData
from users.models import KidsProfile
import bootstrap_datepicker_plus as datetimepicker


class ShoesDataForm(forms.ModelForm):
    class Meta:
        model = ShoesData
        fields = ('kidsProfile', 'buy_date', 'shoes_size', 'shoes_memo', 'shoes_image')
        widgets = {
            'buy_date': datetimepicker.DatePickerInput(
                           format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(ShoesDataForm, self).__init__(*args, **kwargs)
        self.fields['kidsProfile'] = forms.ModelChoiceField(queryset=KidsProfile.objects.filter(user=user))

class ShoesDataEditForm(forms.ModelForm):
    class Meta:
        model = ShoesData
        fields = ('buy_date', 'shoes_size', 'shoes_memo', 'shoes_image')
        widgets = {
            'buy_date': datetimepicker.DatePickerInput(
                           format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        kidsProfileId = kwargs.pop('kidsProfileId','')
        super(ShoesDataEditForm, self).__init__(*args, **kwargs)