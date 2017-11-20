from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class EditTaskForm(forms.Form):
    renewal_date = forms.DateField(help_text="Укажите дату")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом). 
        if data < datetime.date.time.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Помните, что всегда на до возвращать "очищенные" данные.
        return data