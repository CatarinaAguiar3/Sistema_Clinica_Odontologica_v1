from django import forms
from .models import AgendaTrabalho, Procedimento

# Essa classe vai personalizar como o horário é exibido no admin do Django.
class AgendaTrabalhoForm(forms.ModelForm):

    class Meta:
        model = AgendaTrabalho
        fields = '__all__'
        # Defini como serão os campos de horário. 
        # Precisei fazer isso, pois o Django não estava dando muita liberdade para escolher qualquer horário
        widgets = {
            'horario_inicio': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
            'horario_fim': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }

from django import forms
from .models import Procedimento

class ProcedimentoForm(forms.ModelForm):

    class Meta:
        model = Procedimento
        fields = '__all__'

        widgets = {
            'tempo_estimado': forms.NumberInput(
                attrs={
                    'min': 5,
                    'max': 240,
                    'step': 5,
                    'placeholder': 'Tempo em minutos'
                }
            )
        }
