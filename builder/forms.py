from django import forms
from .models import HomeProject,HomeMaterial,LaborCost

class HomeProjectForm(forms.ModelForm):
    class Meta:
        model = HomeProject
        exclude = ['user']
        # Date select panna calendar varathukaga intha widget thevai
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'finish_date': forms.DateInput(attrs={'type': 'date'}),
        }

    pass
class HomeMaterialForm(forms.ModelForm):
    class Meta:
        model = HomeMaterial
        # User kitta irunthu Material and Quantity mattum vanguna pothum.
        # Home and Total Price-a namma backend-la automatic-a calculate panniduvom.
        fields = ['material', 'quantity']

class LaborCostForm(forms.ModelForm):
    class Meta:
        model = LaborCost
        exclude = ['home']