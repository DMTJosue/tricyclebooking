from django import forms
from Tricycleapp.models import Modele

class ModeleForm(forms.ModelForm):

	class Meta:

		model = Modele

		fields = '__all__'

		widgets = {
		    'name': forms.TextInput(attrs={
		        'class': 'form-control',
		        'placeholder': 'lorem ipsum',
		    }),
		}
